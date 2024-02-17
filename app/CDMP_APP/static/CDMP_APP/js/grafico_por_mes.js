$(document).ready(()=>{
    $.ajax({
        url:"/get/gastos_por_mes",
        type:"GET",
    })
    .done((response)=>{
        let dados = JSON.parse(response)
        const ctx = document.getElementById('chart');
        let dataset=[]
        for(let obj in dados){
            if(obj!="labels" && obj!="teto_gasto_cliente"){
                console.log(dados[obj])
                dataset.push(dados[obj])
            }
        }
        const data = {
            labels: dados.labels,
            datasets: [{
                type: 'bar',
                label:"valor despesa",
                data:dataset
            },{
              type: 'line',
              label:"Teto de gastos   ",
              data:dados.teto_gasto_cliente
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
                  text: 'Despesas por mês'
                }
              }
            },
          };
        new Chart(ctx,config)
    })
})