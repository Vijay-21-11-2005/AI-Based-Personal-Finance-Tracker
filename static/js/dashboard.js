let categoryChart;

document.addEventListener('DOMContentLoaded', () => {
    fetchExpenses();
    fetchPrediction();
    fetchAlerts();

    document.getElementById('budget-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            category: document.getElementById('budget-category').value,
            amount: document.getElementById('budget-amount').value
        };

        const response = await fetch('/api/budgets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            fetchAlerts();
        }
    });

    document.getElementById('expense-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            amount: document.getElementById('amount').value,
            note: document.getElementById('note').value,
            category: document.getElementById('category').value
        };

        const response = await fetch('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            document.getElementById('expense-form').reset();
            fetchExpenses();
            fetchPrediction();
            fetchAlerts();
        }
    });
});

async function fetchAlerts() {
    const response = await fetch('/api/alerts');
    const alerts = await response.json();
    const container = document.getElementById('alerts-container');
    
    if (alerts.length > 0) {
        container.classList.remove('hidden');
        container.innerHTML = alerts.map(alert => `
            <div class="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-lg shadow-sm">
                <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-amber-500 mr-3"></i>
                    <p class="text-sm text-amber-800 font-medium">${alert}</p>
                </div>
            </div>
        `).join('');
    } else {
        container.classList.add('hidden');
    }
}

async function fetchExpenses() {
    const response = await fetch('/api/expenses');
    const expenses = await response.json();
    updateDashboard(expenses);
}

async function fetchPrediction() {
    const response = await fetch('/api/predict');
    const data = await response.json();
    document.getElementById('predicted-spending').innerText = `$${data.predicted_spending.toFixed(2)}`;
}

function updateDashboard(expenses) {
    const tableBody = document.getElementById('expense-table-body');
    tableBody.innerHTML = '';

    let totalSpent = 0;
    const categories = {};

    expenses.forEach(exp => {
        totalSpent += exp.amount;
        categories[exp.category] = (categories[exp.category] || 0) + exp.amount;

        const row = `
            <tr class="hover:bg-slate-50 transition-colors">
                <td class="px-4 py-3 text-sm text-slate-600">${new Date(exp.date).toLocaleDateString()}</td>
                <td class="px-4 py-3 text-sm text-slate-800 font-medium">${exp.note}</td>
                <td class="px-4 py-3">
                    <span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-50 text-blue-600">
                        ${exp.category}
                    </span>
                </td>
                <td class="px-4 py-3 text-sm text-right font-bold text-slate-800">$${exp.amount.toFixed(2)}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
    });

    document.getElementById('total-spent').innerText = `$${totalSpent.toFixed(2)}`;
    
    // Top category
    const topCat = Object.entries(categories).sort((a,b) => b[1] - a[1])[0];
    document.getElementById('top-category').innerText = topCat ? topCat[0] : '-';

    updateChart(categories);
}

function updateChart(categories) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChart) {
        categoryChart.destroy();
    }

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: [
                    '#93032E', '#b00438', '#5a021c', '#151515', '#4a4a4a', '#8b5cf6'
                ],
                borderColor: '#1a1a1a',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        color: '#94a3b8'
                    }
                }
            },
            cutout: '70%'
        }
    });
}
