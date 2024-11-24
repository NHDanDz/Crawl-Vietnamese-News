const NewsAnalytics = ({ articles }) => {
    const canvasRef = React.useRef(null);
    const [chartInstance, setChartInstance] = React.useState(null);

    React.useEffect(() => {
        // Tính toán thống kê
        const stats = {};
        articles.forEach(article => {
            stats[article.source] = (stats[article.source] || 0) + 1;
        });

        const data = {
            labels: Object.keys(stats),
            datasets: [{
                label: 'Số lượng bài viết',
                data: Object.values(stats),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };

        // Nếu đã có chart cũ, destroy nó
        if (chartInstance) {
            chartInstance.destroy();
        }

        // Tạo chart mới
        if (canvasRef.current) {
            const ctx = canvasRef.current.getContext('2d');
            const newChart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            setChartInstance(newChart);
        }

        // Cleanup khi component unmount
        return () => {
            if (chartInstance) {
                chartInstance.destroy();
            }
        };
    }, [articles]);

    return React.createElement('div', { className: "container mt-4" },
        // Thống kê tổng quan
        React.createElement('div', { className: "row mb-4" },
            React.createElement('div', { className: "col-md-4" },
                React.createElement('div', { className: "card bg-primary text-white" },
                    React.createElement('div', { className: "card-body text-center" },
                        React.createElement('h5', { className: "card-title" }, "Tổng số bài viết"),
                        React.createElement('p', { className: "display-4" }, articles.length)
                    )
                )
            )
        ),

        // Biểu đồ thống kê
        React.createElement('div', { className: "card mb-4" },
            React.createElement('div', { className: "card-body" },
                React.createElement('h3', { className: "card-title" }, "Phân bố bài viết theo nguồn tin"),
                React.createElement('div', { style: { height: '400px' } },
                    React.createElement('canvas', { ref: canvasRef })
                )
            )
        )
    );
};

// Export component
window.NewsAnalytics = NewsAnalytics;   