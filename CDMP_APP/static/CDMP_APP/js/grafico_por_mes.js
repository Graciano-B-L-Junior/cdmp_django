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
            if(obj!="labels"){
                console.log(obj)
                console.log(dados[obj])
                dataset.push(dados[obj])
            }
        }
        const data = {
            labels: dados.labels,
            datasets: [{
                label:"valor despesa",
                data:dataset
            }]
        };
        const config = {
            type: 'bar',
            data: data,
            options: {
              responsive: true,
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