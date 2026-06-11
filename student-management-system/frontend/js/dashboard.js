document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await apiRequest('/dashboard');
        if (response.success) {
            document.getElementById('total-students').textContent = response.data.total_students;
            document.getElementById('male-students').textContent = response.data.male_students;
            document.getElementById('female-students').textContent = response.data.female_students;
            document.getElementById('avg-cgpa').textContent = response.data.average_cgpa;
        }
    } catch (error) {
        showAlert(error.message || 'Failed to load dashboard statistics.', 'danger');
    }
});
