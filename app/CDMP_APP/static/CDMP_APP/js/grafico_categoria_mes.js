$(document).ready(()=>{
    const ctx = document.getElementById('chart_3');
    $.ajax({
      url:"get/gastos_por_categoria",
      type:"GET",
  }).done((response)=>{
    let dados = response
    const data = {
      labels: Object.keys(dados),
      datasets: [
          {
          label: 'R$',
          data: Object.values(dados),
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
            text: 'Gastos por categoria mês atual'
          }
        }
      },
    };
  
  new Chart(ctx,config)
  })
    
    
})