# tests/test_tasks.py
import json
from app.models.task import Task

def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client):
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'completed': False
    }
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    assert response.json['title'] == task_data['title']
    assert response.json['description'] == task_data['description']
    assert response.json['completed'] == task_data['completed']

def test_create_task_missing_title(client):
    response = client.post('/api/tasks', json={'description': 'No title'})
    assert response.status_code == 400
    assert response.json['error'] == 'Title is required'

def test_get_task(client):
    # First create a task
    task_data = {'title': 'Test Task', 'description': 'Test Description'}
    response = client.post('/api/tasks', json=task_data)
    task_id = response.json['id']
    
    # Get the task
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == task_data['title']

def test_get_task_not_found(client):
    response = client.get('/api/tasks/999')
    assert response.status_code == 404

def test_update_task(client):
    # Create a task
    task_data = {'title': 'Original Title', 'description': 'Original Description'}
    response = client.post('/api/tasks', json=task_data)
    task_id = response.json['id']
    
    # Update the task
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description',
        'completed': True
    }
    response = client.put(f'/api/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['title'] == update_data['title']
    assert response.json['description'] == update_data['description']
    assert response.json['completed'] == update_data['completed']

def test_delete_task(client):
    # Create a task
    response = client.post('/api/tasks', json={'title': 'Task to Delete'})
    task_id = response.json['id']
    
    # Delete the task
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted'
    
    # Verify task is deleted
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 404