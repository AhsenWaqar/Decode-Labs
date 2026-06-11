let currentPage = 1;
const limit = 10;
let currentSearch = '';
let currentSort = '';

document.addEventListener('DOMContentLoaded', () => {
    loadStudents();

    document.getElementById('search-input').addEventListener('keyup', (e) => {
        currentSearch = e.target.value;
        currentPage = 1;
        loadStudents();
    });

    document.querySelectorAll('th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            currentSort = th.getAttribute('data-sort');
            currentPage = 1;
            loadStudents();
        });
    });

    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadStudents();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadStudents();
    });
});

async function loadStudents() {
    try {
        const queryParams = new URLSearchParams({
            page: currentPage,
            limit: limit,
            search: currentSearch,
            sort: currentSort
        });

        const response = await apiRequest(`/students?${queryParams}`);
        if (response.success) {
            renderStudents(response.data.students);
            updatePagination(response.data.total);
        }
    } catch (error) {
        showAlert('Failed to load students.', 'danger');
    }
}

function renderStudents(students) {
    const tbody = document.getElementById('students-tbody');
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No students found.</td></tr>';
        return;
    }

    students.forEach(student => {
        const tr = document.createElement('tr');
        
        // Secure way to handle DOM injection to avoid XSS
        const tdName = document.createElement('td');
        tdName.textContent = student.full_name;
        
        const tdEmail = document.createElement('td');
        tdEmail.textContent = student.email;
        
        const tdCourse = document.createElement('td');
        tdCourse.textContent = student.course;
        
        const tdSemester = document.createElement('td');
        tdSemester.textContent = student.semester;
        
        const tdCgpa = document.createElement('td');
        tdCgpa.textContent = student.cgpa.toFixed(2);
        
        const tdActions = document.createElement('td');
        tdActions.className = 'action-links';
        
        const viewLink = document.createElement('a');
        viewLink.href = `/details.html?id=${student.id}`;
        viewLink.textContent = 'View';
        
        const editLink = document.createElement('a');
        editLink.href = `/add-student.html?id=${student.id}`;
        editLink.textContent = 'Edit';
        
        const deleteLink = document.createElement('a');
        deleteLink.href = 'javascript:void(0)';
        deleteLink.className = 'delete';
        deleteLink.textContent = 'Delete';
        deleteLink.onclick = () => deleteStudent(student.id);

        tdActions.appendChild(viewLink);
        tdActions.appendChild(editLink);
        tdActions.appendChild(deleteLink);

        tr.appendChild(tdName);
        tr.appendChild(tdEmail);
        tr.appendChild(tdCourse);
        tr.appendChild(tdSemester);
        tr.appendChild(tdCgpa);
        tr.appendChild(tdActions);

        tbody.appendChild(tr);
    });
}

function updatePagination(total) {
    const totalPages = Math.ceil(total / limit) || 1;
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
    
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage >= totalPages;
}

async function deleteStudent(id) {
    if (confirm('Are you sure you want to delete this student?')) {
        try {
            const response = await apiRequest(`/students/${id}`, { method: 'DELETE' });
            if (response.success) {
                showAlert(response.message, 'success');
                loadStudents();
            }
        } catch (error) {
            showAlert(error.message || 'Failed to delete student.', 'danger');
        }
    }
}
