document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const studentId = urlParams.get('id');

    if (!studentId) {
        showAlert('No student ID provided.', 'danger');
        return;
    }

    try {
        const response = await apiRequest(`/students/${studentId}`);
        if (response.success) {
            renderProfile(response.data);
            document.getElementById('edit-btn').href = `/add-student.html?id=${studentId}`;
        }
    } catch (error) {
        showAlert(error.message || 'Failed to load student details.', 'danger');
    }
});

function renderProfile(student) {
    document.getElementById('profile-card').style.display = 'block';
    
    // Set initial
    document.getElementById('avatar-initial').textContent = student.full_name.charAt(0).toUpperCase();
    
    // Header
    document.getElementById('profile-name').textContent = student.full_name;
    document.getElementById('profile-course').textContent = `${student.course} - Semester ${student.semester}`;
    
    // Details
    document.getElementById('detail-email').textContent = student.email;
    document.getElementById('detail-phone').textContent = student.phone;
    document.getElementById('detail-gender').textContent = student.gender;
    document.getElementById('detail-cgpa').textContent = student.cgpa.toFixed(2);
    
    const date = new Date(student.created_at);
    document.getElementById('detail-date').textContent = date.toLocaleDateString();
}
