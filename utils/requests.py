
import json
import uuid

class Requests():
    def get(self, **kwargs) -> list[dict]:
        file = open('./server.json')

        data: dict = json.load(file)

        if 'id' in kwargs:
            id = kwargs.get('id')
            
            filtered_data = list(filter(lambda item_temp: item_temp.get('id') == id, data))

            return filtered_data

        return data

    def post(self, data: dict) -> bool:
        prev_data = self.get()

        data['id'] = str(uuid.uuid4())

        new_data = [*prev_data, data]

        with open('./server.json', 'w') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)

        return {
            'message': 'Item created successfully',
            'status_code': 200
        }


    def put(self, **kwargs) -> dict:
        if not 'id' in kwargs:
            return {
               'message': 'Missing id',
               'status_code': 400,
            }

        id = kwargs.get('id')

        try:
        
            all_data = self.get()
            filtered_item_index = [item for item, data in enumerate(all_data) if id in data.values()][0]
            current_item = all_data[filtered_item_index]

            current_item['name'] = kwargs.get('name')
            current_item['permalink'] = kwargs.get('permalink')
            current_item['items'] = kwargs.get('items')

            with open('./server.json', 'w') as file:
                json.dump(all_data, file, ensure_ascii=False, indent=4)

            return {
                'message': 'Item updated successfully',
                'status_code': 200,
            }
        except Exception as error:
            print(error)

            return {
                'message': f'Invalid id',
                'status_code': 404,
            }

    def delete(self, **kwargs):
        if not 'id' in kwargs:
            return {
               'message': 'Missing id',
               'status_code': 400,
            }

        id = kwargs.get('id')

        all_data = self.get()

        filtered_data = list(filter(lambda item_temp: item_temp.get('id') != id, all_data))

        if not self.get(id=id):
            return {
               'message': 'Item not found',
               'status_code': 404,
            }

        with open('./server.json', 'w') as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)

        return {
            'message': 'Item deleted successfully',
            'status_code': 200,
        }


