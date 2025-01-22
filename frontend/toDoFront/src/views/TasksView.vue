<template>
    <div class="tasks_container">
        <div class="tasks_header">
            <input 
                v-model="newTask"
                type="text"
                placeholder="Enter task..."
                class="task-input"
                @keyup.enter="createTask"
            />
            <button @click="createTask", class="add-button">+</button>
        </div>

        <div class="tasks-list">
            <div 
                v-for="task in tasks"
                :key="task.id" 
                class="tasl-item" 
            >
                <div class="task_text">
                    {{ task.title }}
                </div>
                <button class="complete-button" @onclick="completeTask(task.id)">Выполнено</button>
            </div> 
        </div>
    </div>

</template>

<script>
export default {
    name: "TasksView",
    data() {
        return {
            tasks: [],
            newTask: ''
        }
    },
    async mounted() {
        await this.fetchTasks()
    },
    methods: {
        async fetchTasks() {
            const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
            
        },
    }

}

</script>