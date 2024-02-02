$(document).ready(()=>{
    const ctx = document.getElementById('chart_4');
    $.ajax({
      url:"get/gastos_por_categoria_x_teto_categoria",
      type:"GET",
  }).done((response)=>{
    let dados = response
    const data = {
      labels: Object.keys(dados),
      datasets: [
        {
        label: 'Teto',
        data: Object.values(dados).map( (dado)=>dado.teto ),
        backgroundColor:'rgba(122, 214, 66, 0.6)'
        },
        {
        label: 'Gastos',
        backgroundColor: 'rgba(215, 66, 66, 0.6)',
        data: Object.values(dados).map( (dado)=>dado.gastos ),
        },
      ]
  };
  const config = {
      type: 'bar',
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
            text: 'Gastos por categoria mês atual'
          }
        }
      },
    };
  
  new Chart(ctx,config)
  })
    
    
})