function saveDegree() {
    const programName = document.getElementById('degree_name').value.trim();
    if (programName === '') {
        alert('Program name is required');
        return;
    }

    const existing = localStorage.getItem('degree_in_progress');
    const degree = existing ? JSON.parse(existing) : { sections: [] };

    if (degree.sections.length === 0) {
        alert('At least one section is required');
        return;
    }

    degree.program = programName;
    degree.excluded_subjects = document.getElementById('excluded_subjects').value.split(',').map(s => s.trim()).filter(s => s.length > 0);
    degree.excluded_courses = document.getElementById('excluded_courses').value.split(',').map(s => s.trim()).filter(s => s.length > 0);
    localStorage.setItem('degree_in_progress', JSON.stringify(degree));
    fetch('/create-degree/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(degree)
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        if (data.redirect) {
            localStorage.removeItem('degree_in_progress');
            window.location.href = data.redirect;
        } else if (data.error) {
            alert(data.error);
        }
    });
}

function loadDegree() {
    const existing = localStorage.getItem('degree_in_progress');
    if (existing) {
        const degree = JSON.parse(existing);
        document.getElementById('degree_name').value = degree.program || '';
        document.getElementById('excluded_subjects').value = (degree.excluded_subjects || []).join(', ');
        document.getElementById('excluded_courses').value = (degree.excluded_courses || []).join(', ');
        renderSections(degree.sections);
    }
}

window.addEventListener('load', function() {
    loadDegree();
});

function renderSections(sections) {
    const sectionsDiv = document.querySelector('.sections');
    sectionsDiv.innerHTML = '';
    sections.forEach(function(section, index) {
        sectionsDiv.insertAdjacentHTML('beforeend', `
            <div class="section-item">
                <a href="/create-section/?edit=${index}">${section.name}</a>
                <button onclick="deleteSection(${index})">Delete</button>
            </div>
        `);
    });
}

function deleteSection(index) {
    const degree = JSON.parse(localStorage.getItem('degree_in_progress'));
    degree.sections.splice(index, 1);
    degree.sections.forEach(function(sec, i) { sec.priority = i + 1; });
    localStorage.setItem('degree_in_progress', JSON.stringify(degree));
    renderSections(degree.sections);
}