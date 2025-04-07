document.addEventListener('DOMContentLoaded', function() {
    const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        mode: 'python',
        theme: 'dracula',
        lineNumbers: true
    });

    document.querySelectorAll('.task-item').forEach(item => {
        item.addEventListener('click', () => {
            const taskId = item.getAttribute('data-id');
            const task = {{tasks | tojson}}.find(t => t.id == taskId);

            document.getElementById('task-description').innerHTML = `
                <h2>${task.title}</h2>
                <p>${task.description}</p>
                <h3>Тесты:</h3>
                <ul>
                    ${task.tests.map(test => `<li>${test}</li>`).join('')}
                </ul>
            `;

            editor.setValue('');
        });
    });
});

function checkCode() {
    const code = editor.getValue();
    const taskId = document.querySelector('.task-item.active')?.getAttribute('data-id');

    if (!taskId) {
        alert('Сначала выберите задачу!');
        return;
    }

    fetch('/check', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `code=${encodeURIComponent(code)}&task_id=${taskId}`
    })
    .then(response => response.json())
    .then(results => {
        let html = '';
        results.forEach(result => {
            html += `
                <div class="result-item ${result.success ? 'success' : 'error'}">
                    <strong>Тест:</strong> ${result.test_case}<br>
                    <strong>Вывод:</strong> ${result.output}
                </div>
            `;
        });
        document.getElementById('results').innerHTML = html;
    });
}