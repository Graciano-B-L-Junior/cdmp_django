$(document).ready(()=>{
    $.ajax({
        url:"/get/economias_por_mes",
        type:"GET",
    })
    .done((response)=>{
        let dados = JSON.parse(response)
        const ctx = document.getElementById('chart_2');
        var colors = []
        for(var i = 0; i < dados.economias.length; i++){
          var color;
          color = dados.economias[i] > 0 ? "rgba(71, 255, 71, 0.35)" : "rgba(255, 0, 0, 0.49)"
          colors[i] = color;
        }
        const data = {
            labels: dados.labels,
            datasets: [{
                backgroundColor:colors,
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