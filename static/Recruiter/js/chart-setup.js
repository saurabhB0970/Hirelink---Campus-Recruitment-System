document.addEventListener('DOMContentLoaded', function () {
    
    // 1. HIRING FUNNEL (Horizontal Bar)
    const funnelCtx = document.getElementById('funnelChart').getContext('2d');
    const funnelGradient = funnelCtx.createLinearGradient(0, 0, 400, 0);
    funnelGradient.addColorStop(0, '#2563EB');
    funnelGradient.addColorStop(1, '#6366F1');

    new Chart(funnelCtx, {
        type: 'bar',
        data: {
            labels: ['Applied', 'Screened', 'Interviewed', 'Placed'],
            datasets: [{
                label: 'Students',
                data: window.funnelData || [450, 280, 120, 68],
                backgroundColor: funnelGradient,
                borderRadius: 10,
                barThickness: 30
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
        }
    });

    // 2. DEPARTMENT HIRES (Doughnut)
    const deptCtx = document.getElementById('deptChart');
    new Chart(deptCtx, {
        type: 'doughnut',
        data: {
            labels: window.deptLabels || ['CS', 'Electrical', 'E&TC', 'Mech'],
            datasets: [{
                data: window.deptData || [35, 20, 10, 3],
                backgroundColor: ['#2563eb', '#7c3aed', '#ec4899', '#f59e0b'],
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%'
        }
    });

    // 3. PLACEMENT TREND (Line Chart with Area Gradient)
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    const areaGradient = trendCtx.createLinearGradient(0, 0, 0, 400);
    areaGradient.addColorStop(0, 'rgba(37, 99, 235, 0.3)');
    areaGradient.addColorStop(1, 'rgba(37, 99, 235, 0)');

    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Hired per Month',
                data: window.trendData || [8, 15, 30, 55, 42, 68],
                borderColor: '#2563eb',
                backgroundColor: areaGradient,
                fill: true,
                tension: 0.4,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});