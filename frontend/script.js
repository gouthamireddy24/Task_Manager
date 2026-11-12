const API_URL = "http://127.0.0.1:8000/tasks";

const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const filter = document.getElementById("filter");


// Get all tasks from backend
async function loadTasks() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Unable to load tasks");
        }

        const tasks = await response.json();

        displayTasks(tasks);

    } catch (error) {
        taskList.innerHTML =
            `<p class="empty-message">Unable to connect to server.</p>`;

        console.error(error);
    }
}


// Display tasks on the page
function displayTasks(tasks) {

    const selectedFilter = filter.value;

    const filteredTasks = tasks.filter(task => {
        if (selectedFilter === "All") {
            return true;
        }

        return task.status === selectedFilter;
    });

    taskList.innerHTML = "";

    if (filteredTasks.length === 0) {
        taskList.innerHTML =
            `<p class="empty-message">No tasks available.</p>`;
        return;
    }

    filteredTasks.forEach(task => {

        const card = document.createElement("div");
        card.className = "task-card";

        const title = document.createElement("h3");
        title.textContent = task.title;

        const description = document.createElement("p");
        description.textContent = task.description || "No description";

        const status = document.createElement("span");
        status.className = "task-status " +
            (task.status === "Completed" ? "completed" : "pending");
        status.textContent = task.status;

        const editButton = document.createElement("button");
        editButton.className = "edit-btn";
        editButton.textContent = "Edit";
        editButton.onclick = () => editTask(task);

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteTask(task.id);

        card.append(title, description, status);

        if (task.status === "Pending") {
            const completeButton = document.createElement("button");
            completeButton.className = "complete-btn";
            completeButton.textContent = "Complete";
            completeButton.onclick = () => completeTask(task.id);

            card.appendChild(completeButton);
        }

        card.append(editButton, deleteButton);

        taskList.appendChild(card);
    });
}


// Add new task
taskForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title) {
        alert("Please enter a task title");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });

        if (!response.ok) {
            throw new Error("Unable to add task");
        }

        taskForm.reset();
        loadTasks();

    } catch (error) {
        alert(error.message);
    }
});


// Edit task
async function editTask(task) {

    const newTitle = prompt("Enter new task title:", task.title);

    if (newTitle === null) return;

    if (!newTitle.trim()) {
        alert("Task title cannot be empty");
        return;
    }

    const newDescription = prompt(
        "Enter new description:",
        task.description || ""
    );

    if (newDescription === null) return;

    try {
        const response = await fetch(`${API_URL}/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newTitle.trim(),
                description: newDescription.trim()
            })
        });

        if (!response.ok) {
            throw new Error("Unable to update task");
        }

        loadTasks();

    } catch (error) {
        alert(error.message);
    }
}


// Delete task
async function deleteTask(taskId) {

    const confirmDelete = confirm("Are you sure you want to delete this task?");

    if (!confirmDelete) return;

    try {
        const response = await fetch(`${API_URL}/${taskId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Unable to delete task");
        }

        loadTasks();

    } catch (error) {
        alert(error.message);
    }
}


// Mark task as completed
async function completeTask(taskId) {

    try {
        const response = await fetch(
            `${API_URL}/${taskId}/complete`,
            { method: "PATCH" }
        );

        if (!response.ok) {
            throw new Error("Unable to complete task");
        }

        loadTasks();

    } catch (error) {
        alert(error.message);
    }
}


// Filter tasks
filter.addEventListener("change", loadTasks);


// Load tasks when page opens
loadTasks();