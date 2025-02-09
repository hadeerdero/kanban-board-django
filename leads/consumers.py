
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class KanbanConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("kanban", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("kanban", self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.channel_layer.group_send(
#             "kanban",
#             {
#                 "type": "kanban_update",
#                 "data": data,
#             },
#         )

#     async def kanban_update(self, event):
#         await self.send(text_data=json.dumps(event["data"]))

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class KanbanConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         lead_id = data.get("lead_id")
#         new_stage_id = data.get("new_stage_id")

#         # Update the lead's stage in the database
#         from .models import Lead
#         lead = await database_sync_to_async(Lead.objects.get)(id=lead_id)
#         lead.stage_id = new_stage_id
#         await database_sync_to_async(lead.save)()

#         # Notify all connected clients about the update
#         await self.channel_layer.group_send(
#             "kanban_group",
#             {
#                 "type": "lead_moved",
#                 "lead_id": lead_id,
#                 "new_stage_id": new_stage_id,
#             },
#         )

#     async def lead_moved(self, event):
#         await self.send(text_data=json.dumps({
#             "lead_id": event["lead_id"],
#             "new_stage_id": event["new_stage_id"],
#         }))
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async  # Import this
# import json

# class KanbanConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         lead_id = data.get("lead_id")
#         new_stage_id = data.get("new_stage_id")

#         # Update the lead's stage in the database
#         from .models import Lead
#         lead = await database_sync_to_async(Lead.objects.get)(id=lead_id)
#         lead.stage_id = new_stage_id
#         await database_sync_to_async(lead.save)()

#         # Notify all connected clients about the update
#         await self.channel_layer.group_send(
#             "kanban_group",
#             {
#                 "type": "lead_moved",
#                 "lead_id": lead_id,
#                 "new_stage_id": new_stage_id,
#             },
#         )

#     async def lead_moved(self, event):
#         await self.send(text_data=json.dumps({
#             "lead_id": event["lead_id"],
#             "new_stage_id": event["new_stage_id"],
#         }))

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class KanbanConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Optional: Retrieve parameters from the WebSocket URL
        self.lead_id = self.scope["url_route"]["kwargs"].get("lead_id")
        if self.lead_id:
            # Join a group specific to this lead
            self.group_name = f"lead_{self.lead_id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        else:
            # Join a general Kanban group
            self.group_name = "kanban_group"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

    async def disconnect(self, close_code):
        # Leave the group when the WebSocket disconnects
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Handle messages sent by the client.
        Supports:
        - Moving a lead to a new stage (drag-and-drop on Kanban)
        - Listening for updates on a specific lead
        """
        data = json.loads(text_data)

        # Check if the message is for drag-and-drop
        if "lead_id" in data and "new_stage_id" in data:
            lead_id = data["lead_id"]
            new_stage_id = data["new_stage_id"]

            # Update the lead's stage in the database
            await self.update_lead_stage(lead_id, new_stage_id)

            # Notify the Kanban group about the update
            await self.channel_layer.group_send(
                "kanban_group",
                {
                    "type": "lead_moved",
                    "lead_id": lead_id,
                    "new_stage_id": new_stage_id,
                },
            )
        elif "action" in data and data["action"] == "subscribe_lead_updates":
            # Handle subscribing to a specific lead's updates
            lead_id = data.get("lead_id")
            if lead_id:
                await self.channel_layer.group_add(
                    f"lead_{lead_id}",
                    self.channel_name
                )
        else:
            # Handle other types of actions (if needed)
            pass

    async def lead_moved(self, event):
        """
        Send Kanban drag-and-drop updates to WebSocket clients.
        """
        await self.send(text_data=json.dumps({
            "lead_id": event["lead_id"],
            "new_stage_id": event["new_stage_id"],
        }))

    async def lead_update(self, event):
        """
        Send lead-specific updates to WebSocket clients.
        """
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def update_lead_stage(self, lead_id, new_stage_id):
        """
        Update the stage of a lead in the database.
        """
        from .models import Lead
        lead = Lead.objects.get(id=lead_id)
        lead.stage_id = new_stage_id
        lead.save()
