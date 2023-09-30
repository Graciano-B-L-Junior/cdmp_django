$(document).ready(()=>{
    const ctx = document.getElementById('chart_3');
    const DATA_COUNT = 5;
    const NUMBER_CFG = {count: DATA_COUNT, min: 0, max: 100};
    const data = {
        labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
        datasets: [
            {
            label: 'Dataset 1',
            data: [100,50,75,20,10],
            backgroundColor: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
            }
        ]
    };
    const config = {
        type: 'pie',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Gastos por categoria'
            }
          }
        },
      };
    
    new Chart(ctx,config)
    
})