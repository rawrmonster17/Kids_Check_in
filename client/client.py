import requests
import json

BASE_URL = "http://localhost:8000"

def create_kid(first_name, last_name, allergies, checked_in):
    url = f"{BASE_URL}/kids/"
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "allergies": allergies,
        "checked_in": checked_in
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    print(f"Create Kid Response: {response_data}")
    if response.status_code != 200:
        raise Exception(f"Error creating kid: {response_data}")
    return response_data

def create_parent(first_name, last_name, phone_number, email):
    url = f"{BASE_URL}/parents/"
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "email": email
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    print(f"Create Parent Response: {response_data}")
    if response.status_code != 200:
        raise Exception(f"Error creating parent: {response_data}")
    return response_data

def link_parent_kid(parent_id, kid_id):
    url = f"{BASE_URL}/parent_kid/"
    payload = {
        "parent_id": parent_id,
        "kid_id": kid_id
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    print(f"Link Parent Kid Response: {response_data}")
    if response.status_code != 200:
        raise Exception(f"Error linking parent and kid: {response_data}")
    return response_data

def get_kids():
    url = f"{BASE_URL}/kids/"
    response = requests.get(url)
    response_data = response.json()
    print(f"Get Kids Response: {response_data}")
    return response_data

def get_parents():
    url = f"{BASE_URL}/parents/"
    response = requests.get(url)
    response_data = response.json()
    print(f"Get Parents Response: {response_data}")
    return response_data

def get_kids_by_parent(parent_id):
    url = f"{BASE_URL}/parent_kids/{parent_id}"
    response = requests.get(url)
    response_data = response.json()
    print(f"Get Kids by Parent Response: {response_data}")
    return response_data

def main():
    try:
        # Scenario 1: 1 Kid with 1 Parent
        kid1 = create_kid("Alice", "Smith", "None", True)
        parent1 = create_parent("John", "Smith", "123-456-7890", "john.smith@example.com")
        link_parent_kid(parent1["id"], kid1["id"])

        # Scenario 2: 2 Kids Attached to 1 Parent
        kid2 = create_kid("Bob", "Brown", "Dairy", True)
        kid3 = create_kid("Charlie", "Brown", "Gluten", True)
        parent2 = create_parent("Sarah", "Brown", "987-654-3210", "sarah.brown@example.com")
        link_parent_kid(parent2["id"], kid2["id"])
        link_parent_kid(parent2["id"], kid3["id"])

        # Verification
        print("Kids:")
        print(json.dumps(get_kids(), indent=2))
        
        print("Parents:")
        print(json.dumps(get_parents(), indent=2))

        print(f"Kids linked to Parent 1 (ID {parent1['id']}):")
        print(json.dumps(get_kids_by_parent(parent1['id']), indent=2))
        
        print(f"Kids linked to Parent 2 (ID {parent2['id']}):")
        print(json.dumps(get_kids_by_parent(parent2['id']), indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
