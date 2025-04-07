function onClickedEstimateExpense() {
    console.log("Predict Insurance Expense button clicked");
  
    const age = document.getElementById("uiAge").value;
    const bmi = document.getElementById("uiBmi").value;
    const children = document.getElementById("uiChildren").value;
    const region = document.getElementById("uiRegion").value;
    const sex = document.getElementById("maleBtn").classList.contains("active") ? "male" : "female";
    const smoker = document.getElementById("yesSmokerBtn").classList.contains("active") ? "yes" : "no";
    const url = "http://127.0.0.1:5000/predict_expense";
  
    $.post(url, {
      age: age,
      bmi: bmi,
      children: children,
      sex: sex,
      smoker: smoker,
      region: region
    }, function(data, status) {
      console.log("Prediction received: ", data.estimated_expense);
      document.getElementById("uiEstimatedExpense").innerHTML =
        "<h2>"+data.estimated_expense.toString()+" Dollars</h2>";
    });
  }
  
  function onPageLoad() {
    console.log("Document loaded");
    const url = "http://127.0.0.1:5000/get_metadata";
    $.get(url, function(data, status) {
      console.log("Got region names:", data.regions);
      if (data.regions) {
        const uiRegion = document.getElementById("uiRegion");
        $('#uiRegion').empty();
        data.regions.forEach(function(region) {
          const opt = new Option(region);
          $('#uiRegion').append(opt);
        });
      }
    });
  }
  
  // Toggle button logic
  function setupToggleButtons() {
    $(".toggle-btn").click(function () {
      const group = $(this).parent();
      group.find(".toggle-btn").removeClass("active");
      $(this).addClass("active");
    });
  }
  
  window.onload = function () {
    onPageLoad();
    setupToggleButtons();
  };
  