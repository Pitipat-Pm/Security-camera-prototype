const stopForm = document.getElementById('stopForm');
const resetForm = document.getElementById('resetForm');
const statusMsg = document.getElementById('statusMsg');

function setMode(mode) {
    const formData = new FormData();
    formData.append('mode', mode);

    fetch('/start', {
        method: 'POST',
        body: formData
    }).then(resp => {
        if (resp.ok) {
            statusMsg.innerText = `Mode '${mode}' started.`;
            refreshFileLists();
            if (mode === 'photo') {
                setTimeout(refreshLatestPhoto, 800);
            }
        }
    }).catch(err => {
        statusMsg.innerText = `Error starting mode: ${err}`;
    });
}

function refreshFileLists() {
    fetch('/file_lists')
        .then(resp => resp.text())
        .then(html => {
            document.getElementById('fileLists').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('fileLists').innerHTML = '<p>Error loading files</p>';
        });
}

function refreshLatestPhoto() {
    fetch('/latest_photo')
        .then(resp => resp.json())
        .then(data => {
            if (data.path) {
                document.getElementById('latestPhoto').innerHTML =
                    `<h3>Latest Photo:</h3><img src="/view_file?path=${encodeURIComponent(data.path)}" width="320">`;
            }
        });
}

function deleteFile(folder, filename) {
    if (!confirm(`Delete ${filename}?`)) return;
    fetch(`/delete/${folder}/${filename}`, { method: 'POST' })
        .then(() => refreshFileLists());
}

if (stopForm) {
    stopForm.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/stop_save', { method: 'POST' })
            .then(resp => resp.json())
            .then(data => {
                statusMsg.innerText = data.message;
                resetForm.style.display = 'inline';
                stopForm.style.display = 'none';
                refreshFileLists();
                refreshLatestPhoto();
            });
    });
}

if (resetForm) {
    resetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/reset', { method: 'POST' })
            .then(resp => resp.json())
            .then(data => {
                statusMsg.innerText = data.message;
                resetForm.style.display = 'none';
                stopForm.style.display = 'inline';
                refreshFileLists();
            });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    refreshFileLists();
    refreshLatestPhoto();
});
