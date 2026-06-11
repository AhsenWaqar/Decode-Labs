let studentId = null;

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    studentId = urlParams.get('id');

    if (studentId) {
        document.getElementById('page-title').textContent = 'Edit Student';
        // Hide sidebar Add Student active state if editing
        document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
        await loadStudentData(studentId);
    }

    document.getElementById('student-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveStudent();
    });
});

async function loadStudentData(id) {
    try {
        const response = await apiRequest(`/students/${id}`);
        if (response.success) {
            const student = response.data;
            document.getElementById('full_name').value = student.full_name;
            document.getElementById('email').value = student.email;
            document.getElementById('phone').value = student.phone;
            document.getElementById('gender').value = student.gender;
            document.getElementById('course').value = student.course;
            document.getElementById('semester').value = student.semester;
            document.getElementById('cgpa').value = student.cgpa;
        }
    } catch (error) {
        showAlert('Failed to load student data.', 'danger');
    }
}

function clearErrors() {
    document.querySelectorAll('.error-text').forEach(el => {
        el.textContent = '';
        el.style.display = 'none';
    });
}

function showFieldErrors(errors) {
    for (const [field, message] of Object.entries(errors)) {
        const errorEl = document.getElementById(`error-${field}`);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
        }
    }
}

async function saveStudent() {
    clearErrors();
    
    // Frontend validation is partly handled by HTML5 required/min/max/pattern attributes
    const data = {
        full_name: document.getElementById('full_name').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        gender: document.getElementById('gender').value,
        course: document.getElementById('course').value.trim(),
        semester: parseInt(document.getElementById('semester').value),
        cgpa: parseFloat(document.getElementById('cgpa').value)
    };

    try {
        let response;
        if (studentId) {
            response = await apiRequest(`/students/${studentId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        } else {
            response = await apiRequest('/students', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        }

        if (response.success) {
            showAlert(response.message, 'success');
            setTimeout(() => {
                window.location.href = '/students.html';
            }, 1000);
        }
    } catch (error) {
        if (error.errors) {
            showFieldErrors(error.errors);
        }
        showAlert(error.message || 'An error occurred while saving the student.', 'danger');
    }
}
