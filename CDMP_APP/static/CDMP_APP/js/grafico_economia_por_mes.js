$(document).ready(()=>{
    $.ajax({
        url:"/get/economias_por_mes",
        type:"GET",
    })
    .done((response)=>{
        let dados = JSON.parse(response)
        const ctx = document.getElementById('chart_2');
        const data = {
            labels: dados.labels,
            datasets: [{
                type: 'bar',
                label:"Economia",
                data:dados.economias
            }]
        };
        const config = {
            data: data,
            options: {
              responsive: true,
              interaction: {
                intersect: false,
                mode: 'index',
              },
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: 'Economias ou Despesas por mês'
                }
              }
            },
          };
        new Chart(ctx,config)
    })
})