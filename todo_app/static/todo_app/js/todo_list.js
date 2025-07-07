console.log('todo_list.js が読み込まれました');

// ページネーションの表示件数を変更する関数（グローバルスコープ）
function changePerPage(value) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('per_page', value);
    currentUrl.searchParams.set('page', 1); // 表示件数を変えたら最初のページに戻す
    window.location.href = currentUrl.toString();
}

document.addEventListener('DOMContentLoaded', function() {
    const addTodoButton = document.getElementById('add-todo');
    if (addTodoButton) {
        addTodoButton.addEventListener('click', () => {
            const title = document.getElementById('new-todo-title').value;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // 例: HTML に CSRF トークンがある場合
            fetch('{% url todo_create %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ title }),
            })
            .then(response => response.json())
            .then(data => {
                updateTodoList(data.todos);
            });
        });
    }

    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (event) => {
            const todoId = event.target.dataset.todoId;
            const completed = event.target.checked;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // 例: HTML に CSRF トークンがある場合
            fetch(`/todo/update/${todoId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ completed }),
            })
            .then(response => response.json())
            .then(data => {
                updateTodoList(data.todos);
            });
        });
    })

    const updateTodoButton = document.querySelector('.update-todo');
    if (updateTodoButton) {
        updateTodoButton.addEventListener('click', () => {
            const checkedCheckbox = document.querySelector('input[type="checkbox"]:checked');
            if (checkedCheckbox && checkedCheckbox.dataset.todoId) {
                const todoId = checkedCheckbox.dataset.todoId;
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // 例: HTML に CSRF トークンがある場合
                fetch(`/todo/update/${todoId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ completed: true }),
                })
                .then(response => response.json())
                .then(data => {
                    updateTodoList(data.todos);
                });
            }
        });
    }

    // ★ 初期表示のアイコン追加処理 ★
    const initialRows = document.querySelectorAll('#todo-list tr');
    initialRows.forEach((row, index) => {
        const actionCells = row.querySelectorAll('.action-cell');
        const noCell = document.createElement('td');
        noCell.textContent = index + 1;
        row.insertBefore(noCell, row.firstChild);

        const todoId = row.dataset.todoId;
        console.log('Initial todoId:', todoId);
        if (todoId) {
            if (actionCells.length > 0) {
                const editIcon = document.createElement('img');
                editIcon.src = "/static/todo_app/images/edit_icon.png";
                editIcon.alt = "編集";
                editIcon.dataset.todoId = todoId;
                editIcon.style.width = '2em';
                editIcon.style.height = '2em';
                editIcon.style.verticalAlign = 'middle';
                editIcon.style.cursor = 'pointer';
                actionCells[0].appendChild(editIcon);
                console.log('編集アイコンを追加しました (初期表示):', editIcon, 'to', actionCells[0]);
                editIcon.addEventListener('click', function() {
                    const todoId = this.dataset.todoId;
                    console.log('編集アイコンがクリックされました。todoId:', todoId);
                    if (todoId) {
                        window.location.href = `/todo/update/${todoId}/`; // 編集ページの URL
                    }
                });
            }
            if (actionCells.length > 1) {
                const deleteIcon = document.createElement('img');
                deleteIcon.src = "/static/todo_app/images/delete_icon.png";
                deleteIcon.alt = "削除";
                deleteIcon.dataset.todoId = todoId;
                deleteIcon.style.width = '2em';
                deleteIcon.style.height = '2em';
                deleteIcon.style.verticalAlign = 'middle';
                deleteIcon.style.cursor = 'pointer';
                actionCells[1].appendChild(deleteIcon);
                console.log('削除アイコンを追加しました (初期表示):', deleteIcon, 'to', actionCells[1]);
                deleteIcon.addEventListener('click', function() {
                    const todoId = this.dataset.todoId;
                    console.log('削除アイコンがクリックされました。todoId:', todoId);
                    if (todoId) {
                        if (confirm('この Todo を削除しますか？')) {
                            window.location.href = `/todo/delete/${todoId}/`; // 削除処理の URL
                        }
                    }
                });
            }
        }
    });

    function updateTodoList(todos) {
        console.log('updateTodoList called');
        const todoList = document.getElementById('todo-list');
        todoList.innerHTML = '';
        todos.forEach((todo, index) => { // index を追加
            console.log('Processing todo (in updateTodoList):', todo);
            const row = document.createElement('tr');
            row.dataset.todoId = todo.id;
            row.style.backgroundColor = todo.completed ? 'red' : 'yellow';

            const noCell = document.createElement('td');
            noCell.textContent = index + 1; // 連番を設定

            const completedCell = document.createElement('td');
            const completedCheckbox = document.createElement('input');
            completedCheckbox.type = 'checkbox';
            completedCheckbox.checked = todo.completed;
            completedCheckbox.dataset.todoId = todo.id;
            completedCell.appendChild(completedCheckbox);

            const titleCell = document.createElement('td');
            titleCell.textContent = todo.title;

            const actionCells = row.querySelectorAll('.action-cell');
            console.log('actionCells in updateTodoList:', actionCells);

            if (actionCells.length > 0) {
                const editIcon = document.createElement('img');
                editIcon.src = "/static/todo_app/images/edit_icon.png";
                editIcon.alt = "編集";
                editIcon.dataset.todoId = todo.id;
                editIcon.style.width = '2em';
                editIcon.style.height = '2em';
                editIcon.style.verticalAlign = 'middle';
                editIcon.style.cursor = 'pointer';
                actionCells[0].appendChild(editIcon);
                editIcon.addEventListener('click', function() {
                    const todoId = this.dataset.todoId;
                    console.log('編集アイコンがクリックされました (updated list)。todoId:', todoId);
                    if (todoId) {
                        window.location.href = `/todo/update/${todoId}/`; // 編集ページの URL
                    }
                });
            }

            if (actionCells.length > 1) {
                const deleteIcon = document.createElement('img');
                deleteIcon.src = "/static/todo_app/images/delete_icon.png";
                deleteIcon.alt = "削除";
                deleteIcon.dataset.todoId = todo.id;
                deleteIcon.style.width = '2em';
                deleteIcon.style.height = '2em';
                deleteIcon.style.verticalAlign = 'middle';
                deleteIcon.style.cursor = 'pointer';
                actionCells[1].appendChild(deleteIcon);
                deleteIcon.addEventListener('click', function() {
                    const todoId = this.dataset.todoId;
                    console.log('削除アイコンがクリックされました (updated list)。todoId:', todoId);
                    if (todoId) {
                        if (confirm('この Todo を削除しますか？')) {
                            window.location.href = `/todo/delete/${todoId}/`; // 削除処理の URL
                        }
                    }
                });
            }

            row.insertBefore(noCell, row.firstChild); // No. セルを最初に追加
            row.appendChild(completedCell);
            row.appendChild(titleCell);
            todoList.appendChild(row);

            completedCheckbox.addEventListener('change', (event) => {
                const currentTodoId = event.target.dataset.todoId;
                const currentCompleted = event.target.checked;
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // 例: HTML に CSRF トークンがある場合
                fetch(`/todo/update/${currentTodoId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ completed: currentCompleted }),
                })
                .then(response => response.json())
                .then(data => {
                    updateTodoList(data.todos);
                });
            });
        });
    }

    function updateDateTime() {
        const now = new Date();
        const datetimeString = now.toISOString().slice(0, 19).replace('T', ' ');
        const currentDatetimeSpan = document.getElementById('current-datetime');
        if (currentDatetimeSpan) {
            currentDatetimeSpan.textContent = datetimeString;
        }
    }

    updateDateTime();
    setInterval(updateDateTime, 1000);
});