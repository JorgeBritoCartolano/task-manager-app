document.addEventListener('DOMContentLoaded', () => {
    const taskList = document.getElementById('task-list');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskModal = document.getElementById('task-modal');
    const closeModal = document.getElementById('close-modal');
    const taskForm = document.getElementById('task-form');
    const modalTitle = document.getElementById('modal-title');
    const taskIdInput = document.getElementById('task-id');
    const taskTitleInput = document.getElementById('task-title');
    const taskStatusSelect = document.getElementById('task-status');
    const taskDescriptionInput = document.getElementById('task-description');

    let tasks = []; // Here the tasks will be stored

    const apiUrl = '<your-api-url>'; 

    // Function to load tasks from the API
    function loadTasks() {
        fetch(`${apiUrl}`, {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                tasks = data.tasks;  
                renderTasks();  
            })
            .catch(error => console.error('Error loading tasks:', error));
    }

    // Function to render tasks in the UI
    function renderTasks() {
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';

            taskItem.innerHTML = `
                <div>
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                    <p><strong>Status:</strong> ${task.status}</p>
                </div>
                <div class="task-actions">
                    <button class="edit-btn" data-id="${task.taskId}">Edit</button>
                    <button class="delete-btn" data-id="${task.taskId}">Delete</button>
                </div>
            `;

            taskList.appendChild(taskItem);
        });
    }

    // Open the modal to create a new task
    addTaskBtn.addEventListener('click', () => {
        taskIdInput.value = '';
        taskTitleInput.value = '';
        taskStatusSelect.value = 'Pending';
        taskDescriptionInput.value = '';
        modalTitle.textContent = 'New Task';
        taskModal.style.display = 'block';
    });

    // Close the modal
    closeModal.addEventListener('click', () => {
        taskModal.style.display = 'none';
    });

    // Create or update a task
    taskForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const taskData = {
            title: taskTitleInput.value,
            status: taskStatusSelect.value,
            description: taskDescriptionInput.value,
        };

        if (taskIdInput.value) {
            // Update task
            taskData.taskId = taskIdInput.value;
            updateTask(taskData);
        } else {
            // Create new task
            createTask(taskData);
        }
    });

    // Function to create a task in the API
    function createTask(task) {
        fetch(`${apiUrl}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(task)
        })
            .then(response => response.json())
            .then(data => {
                tasks.push(data);
                renderTasks();
                taskModal.style.display = 'none';
            })
            .catch(error => console.error('Error creating task:', error));
    }

    // Function to update a task in the API
    function updateTask(task) {
        fetch(`${apiUrl}/${task.taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(task)
        })
            .then(response => response.json())
            .then(data => {
                const index = tasks.findIndex(t => t.taskId === data.taskId);
                tasks[index] = data;
                renderTasks();
                taskModal.style.display = 'none';
            })
            .catch(error => console.error('Error updating task:', error));
    }

    // Function to delete a task in the API
    function deleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            fetch(`${apiUrl}/${taskId}`, {
                method: 'DELETE'
            })
                .then(() => {
                    tasks = tasks.filter(task => task.taskId !== taskId);
                    renderTasks();
                })
                .catch(error => console.error('Error deleting task:', error));
        }
    }

    // Delegate edit and delete events
    taskList.addEventListener('click', (event) => {
        if (event.target.classList.contains('edit-btn')) {
            const taskId = event.target.dataset.id;
            const task = tasks.find(t => t.taskId === taskId);

            taskIdInput.value = task.taskId;
            taskTitleInput.value = task.title;
            taskStatusSelect.value = task.status;
            taskDescriptionInput.value = task.description;

            modalTitle.textContent = 'Edit Task';
            taskModal.style.display = 'block';
        } else if (event.target.classList.contains('delete-btn')) {
            const taskId = event.target.dataset.id;
            deleteTask(taskId);
        }
    });

    // Load tasks on start
    loadTasks();
});