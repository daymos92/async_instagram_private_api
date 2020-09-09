from ..core.repository import Repository


class LocationRepository(Repository):
    async def info(self, location_id):
        options = {
            'url': f'/api/v1/locations/{location_id}/info/',
        }
        response = await self.client.request.send(**options)
        return response
