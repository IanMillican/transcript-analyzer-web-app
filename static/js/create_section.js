document.addEventListener('change', function(event) {
    if (event.target.classList.contains('operator-select')) {
        const value = event.target.value;
        const node = event.target.parentElement;
        const childrenDiv = node.querySelector(':scope > .children');
        childrenDiv.innerHTML = '';
        childrenDiv.setAttribute('hidden', '');
        if (value === 'and' || value === 'or' || value === 'xor') {
            childrenDiv.removeAttribute('hidden');
            if (childrenDiv.children.length === 0) {
                childrenDiv.insertAdjacentHTML('beforeend', createRequirementNode());
                childrenDiv.querySelector(':scope > .requirement-node > .add-sibling').removeAttribute('hidden');
            }
        } else if (value === 'course') {
            childrenDiv.removeAttribute('hidden');
            if (childrenDiv.children.length === 0) {
                childrenDiv.insertAdjacentHTML('beforeend', createCourseNode());
            }
        } else if (value === 'constraint') {
            childrenDiv.removeAttribute('hidden');
            if (childrenDiv.children.length === 0) {
                childrenDiv.insertAdjacentHTML('beforeend', createConstraintNode());
            }
        } else {
            childrenDiv.setAttribute('hidden', '');
        }
    }
});

function createRequirementNode() {
    return `
        <div class="requirement-node">
            <select class="operator-select">
                <option value="">-- Select --</option>
                <option value="and">All of</option>
                <option value="or">At least one of</option>
                <option value="xor">Exactly one of</option>
                <option value="course">Course</option>
                <option value="constraint">Constraint</option>
            </select>
            <div class="children" hidden></div>
            <button class="add-sibling" hidden>Add requirement</button>
            <button class="remove-node">Remove</button>
        </div>
    `;
}

function createConstraintNode() {
    return `
        <div>
            <ul>
                <li><label>Number of courses: </label><input type="number" class="count" name="count"></li>
                <li><label>Minimum number of credit hours</label><input type="number" class="min_credit_hours" name="min_credit_hours"></li>
                <li><label>Any subjects required for this section: </label><input type="text" class="include_subject" name="include_subject"></li>
                <li><label>Any subjects that can't be included in this section: </label><input type="text" class="exclude_subject" name="exclude_subject"></li>
                <li><label>Minimum 2000 level courses: </label><input type="number" class="min_level_2000" name="min_level_2000"></li>
                <li><label>Minimum 3000 level courses: </label><input type="number" class="min_level_3000" name="min_level_3000"></li>
                <li><label>Minimum 4000 level courses: </label><input type="number" class="min_level_4000" name="min_level_4000"></li>
            </ul>
        </div>
    `
}

function createCourseNode() {
    return `
        <div>
            <ul class = course_entry>
                <li><label>Course Code (Enter in the form of ABC*1234): </label><input type="text" class="course_code" name="course_code"></li>
                <li><label>Course Name: </label><input type="text" class="course_name" name="course_name"></li>
                <li><label>Credit Hours: </label><input type="text" class="credit_hour" name="credit_hour"></li>
            </ul>
        </div>
    `
}

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('add-sibling') || event.target.classList.contains('remove-node')) {
        event.preventDefault();
    }
    if (event.target.classList.contains('add-sibling')) {
        const node = event.target.parentElement;
        const parentChildrenDiv = node.parentElement;
        node.querySelector(':scope > .add-sibling').setAttribute('hidden', '');
        parentChildrenDiv.insertAdjacentHTML('beforeend', createRequirementNode());
        const siblings = parentChildrenDiv.querySelectorAll(':scope > .requirement-node');
        console.log('number of siblings:', siblings.length);
        console.log('last sibling:', siblings[siblings.length - 1]);
        console.log('last sibling add button:', siblings[siblings.length - 1].querySelector(':scope > .add-sibling'));
        siblings[siblings.length - 1].querySelector(':scope > .add-sibling').removeAttribute('hidden');
        node.querySelector(':scope > .add-sibling').setAttribute('hidden', '');
        console.log('first sibling button hidden:', node.querySelector(':scope > .add-sibling').hasAttribute('hidden'));

        function getDepth(el) {
            let depth = 0;
            let current = el;
            while (current.parentElement) {
                if (current.classList.contains('requirement-node')) depth++;
                current = current.parentElement;
            }
            return depth;
        }

        const allAddButtons = document.querySelectorAll('.add-sibling');
        allAddButtons.forEach(function(btn) {
            console.log('button depth:', getDepth(btn), 'hidden:', btn.hasAttribute('hidden'));
        });
    } else if (event.target.classList.contains('remove-node')) {
        const node = event.target.parentElement;
        const parentChildrenDiv = node.parentElement;
        node.remove();
        const siblings = parentChildrenDiv.querySelectorAll(':scope > .requirement-node');
        if (siblings.length > 0) {
            siblings[siblings.length - 1].querySelector(':scope > .add-sibling').removeAttribute('hidden');
        }
    }
});

function buildRequirementJSON(node) {
    const select = node.querySelector(':scope > select.operator-select');
    const value = select.value;
    const childrenDiv = node.querySelector(':scope > .children');

    if (value === 'course') {
        const code = childrenDiv.querySelector('.course_code').value;
        const subject = code.split("*")[0]
        const number = parseInt(code.split("*")[1]);
        const name = childrenDiv.querySelector('.course_name').value;
        const creditHours = parseInt(childrenDiv.querySelector('.credit_hour').value);
        return {
            "Subject": subject,
            "Number": number,
            "Name": name,
            "CreditHours": creditHours,
            "Coop": false
        }
    } else if (value === 'constraint') {
        const count = parseInt(childrenDiv.querySelector('.count').value);
        const minCreditHours = parseInt(childrenDiv.querySelector('.min_credit_hours').value)
        const includeSubject = childrenDiv.querySelector('.include_subject').value.split(",").map(s => s.trim()).filter(s => s.length > 0);
        const excludeSubject = childrenDiv.querySelector('.exclude_subject').value.split(", ").map(s => s.trim()).filter(s => s.length > 0);
        const minLevel2000 = parseInt(childrenDiv.querySelector('.min_level_2000').value)
        const minLevel3000 = parseInt(childrenDiv.querySelector('.min_level_3000').value)
        const minLevel4000 = parseInt(childrenDiv.querySelector('.min_level_4000').value)
        return {
            "constraint": {
                "count": count,
                "min_credit_hours": minCreditHours,
                "include_subject": includeSubject,
                "exclude_subject": excludeSubject,
                "min_level_2000": minLevel2000,
                "min_level_3000": minLevel3000,
                "min_level_4000": minLevel4000
            }
        }
    } else {
        const children = childrenDiv.querySelectorAll(':scope > .requirement-node');
        const childResults = [];
        children.forEach(function(child) {
            childResults.push(buildRequirementJSON(child));
        });
        return { [value]: childResults };
    }

}

function saveSection() {
    // Read the section name from the input
    const sectionName = document.getElementById('section_name').value;

    // Get the root requirement node and build the JSON
    const rootNode = document.querySelector('.requirement-node');
    if (!validateSection(rootNode) || sectionName === "" || sectionName === null) {
        alert('Section name is required');
        return;
    }
    const requirements = buildRequirementJSON(rootNode);

    // Read existing degree from localStorage, or start fresh
    const existing = localStorage.getItem('degree_in_progress');
    const degree = existing ? JSON.parse(existing) : { 
        "program": "", 
        "excluded_subjects": [], 
        "excluded_courses": [], 
        "sections": [] 
    };

    // Check if we're editing an existing section or adding a new one
    const urlParams = new URLSearchParams(window.location.search);
    const editIndex = urlParams.get('edit');

    if (editIndex !== null) {
        // Editing existing section — replace it
        degree.sections[parseInt(editIndex)].name = sectionName;
        degree.sections[parseInt(editIndex)].requirements = requirements;
    } else {
        // New section — append with next priority
        const priority = degree.sections.length + 1;
        degree.sections.push({
            "name": sectionName,
            "priority": priority,
            "requirements": requirements
        });
    }

    // Save back to localStorage
    localStorage.setItem('degree_in_progress', JSON.stringify(degree));

    // Navigate back to create_degree page
    window.location.href = '/create-degree/';
}

function validateSection(root) {
    const select = root.querySelector(':scope > select.operator-select');
    const value = select.value;
    const childrenDiv = root.querySelector(':scope > .children');
    if (value === 'course') {
        const code = childrenDiv.querySelector('.course_code').value;
        const name = childrenDiv.querySelector('.course_name').value;
        const creditHours = childrenDiv.querySelector('.credit_hour').value;
        return code !== '' && name !== '' && creditHours !== '';
    } else if (value === 'constraint') {
        const count = childrenDiv.querySelector('.count').value;
        const minCreditHours = childrenDiv.querySelector('.min_credit_hours').value;
        return count !== '' && minCreditHours !== '';
    } else if (value === '') {
        return false;
    } else {
        let ret = true;
        const children = childrenDiv.querySelectorAll(':scope > .requirement-node');
        for (let i = 0; i < children.length; i++) {
            ret = ret && validateSection(children[i]);
        }
        return ret
    }
}