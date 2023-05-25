import requests



get_url = "https://jsonplaceholder.typicode.com/todos/9"

get_response = requests.get(get_url)
print(get_response.json())

# Put
to_do_item_9 = {"userId" : 2, "title" : "put title", "completed" : True}
put_response = requests.put(get_url, json=to_do_item_9)
print(put_response.json())

# Patch
to_do_item_patch_9 = {"title" : "Patch Test"}
patch_response = requests.patch(get_url, json=to_do_item_patch_9)
print(patch_response.json())


# Delete
delete_response = requests.delete(get_url)
print(delete_response.json())
print(delete_response.status_code)