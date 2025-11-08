/**
 * PaddleCoach - Stats Visualization Module
 * Author: Rakshit
 * Description: Chart.js-based data visualization for player statistics
 */

const StatsVisualizer = {
    charts: {},
    
    // Initialize all charts
    initializeCharts() {
        this.createPerformanceChart();
        this.createShotDistributionChart();
    },
    
    // Create performance trend line chart
    createPerformanceChart() {
        const ctx = document.getElementById('performance-chart');
        if (!ctx) return;
        
        this.charts.performance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                datasets: [{
                    label: 'Win Rate (%)',
                    data: [45, 52, 58, 63, 65, 67],
                    borderColor: 'rgb(37, 99, 235)',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Shot Accuracy (%)',
                    data: [60, 62, 65, 68, 70, 72],
                    borderColor: 'rgb(16, 185, 129)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    },
    
    // Create shot distribution pie chart
    createShotDistributionChart() {
        const ctx = document.getElementById('shot-distribution-chart');
        if (!ctx) return;
        
        this.charts.shotDistribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Forehand', 'Backhand', 'Serve', 'Smash', 'Block', 'Push'],
                datasets: [{
                    data: [35, 25, 15, 10, 10, 5],
                    backgroundColor: [
                        'rgb(37, 99, 235)',
                        'rgb(16, 185, 129)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)',
                        'rgb(139, 92, 246)',
                        'rgb(236, 72, 153)'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                }
            }
        });
    },
    
    // Create bar chart for comparison
    createComparisonChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Your Stats',
                    data: data.player,
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    borderColor: 'rgb(37, 99, 235)',
                    borderWidth: 1
                }, {
                    label: 'Pro Average',
                    data: data.pro,
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgb(16, 185, 129)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    },
    
    // Create radar chart for skill analysis
    createSkillRadarChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        return new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Speed', 'Accuracy', 'Power', 'Spin', 'Consistency', 'Placement'],
                datasets: [{
                    label: 'Your Skills',
                    data: data.player,
                    fill: true,
                    backgroundColor: 'rgba(37, 99, 235, 0.2)',
                    borderColor: 'rgb(37, 99, 235)',
                    pointBackgroundColor: 'rgb(37, 99, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(37, 99, 235)'
                }, {
                    label: 'Target Level',
                    data: data.target,
                    fill: true,
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: 'rgb(16, 185, 129)',
                    pointBackgroundColor: 'rgb(16, 185, 129)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(16, 185, 129)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    },
    
    // Update chart data dynamically
    updateChartData(chartName, newData) {
        const chart = this.charts[chartName];
        if (!chart) return;
        
        chart.data.datasets.forEach((dataset, index) => {
            dataset.data = newData[index];
        });
        
        chart.update();
    },
    
    // Create heatmap for shot placement
    createShotPlacementHeatmap(canvasId, data) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        // Draw table outline
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.strokeRect(0, 0, width, height);
        
        // Draw center line
        ctx.beginPath();
        ctx.moveTo(width / 2, 0);
        ctx.lineTo(width / 2, height);
        ctx.stroke();
        
        // Draw heatmap points
        data.forEach(point => {
            const x = (point.x / 100) * width;
            const y = (point.y / 100) * height;
            const intensity = point.intensity / 100;
            
            const gradient = ctx.createRadialGradient(x, y, 0, x, y, 30);
            gradient.addColorStop(0, `rgba(37, 99, 235, ${intensity})`);
            gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(x - 30, y - 30, 60, 60);
        });
    },
    
    // Destroy chart
    destroyChart(chartName) {
        if (this.charts[chartName]) {
            this.charts[chartName].destroy();
            delete this.charts[chartName];
        }
    },
    
    // Destroy all charts
    destroyAllCharts() {
        Object.keys(this.charts).forEach(chartName => {
            this.destroyChart(chartName);
        });
    }
};

// Initialize charts when this module is loaded
if (typeof initializeCharts === 'function') {
    // Called from player_stats.html
    window.initializeCharts = function() {
        StatsVisualizer.initializeCharts();
    };
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatsVisualizer;
}
