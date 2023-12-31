// update plot via drop down
const updatePlot = () => {
  const dropdownCat = d3.select("#contract-dropdown");
  const category = dropdownCat.property("value");
  plotData(category)
}

// listeners for dropdown
d3.selectAll("#contract-dropdown").on("change", updatePlot);

// Function to loop through the list and create a new list of objects
function createServiceChurnList(data) {
  const serviceChurnList = [];

  // Function to categorize service
  function categorizeService(service) {
      if (service === 'DSL' || service === 'Fiber optic' || service === 'Yes') {
          return 'Yes';
      }
      return 'No';
  }

  // Loop through each customer object
  data.forEach(customer => {
      // Loop through service-related properties
      for (const [service, churn] of Object.entries(customer)) {
          // Check if the property is a service-related property (e.g., online_security, device_protection)
          if (service.includes('service') || service.includes('protection') || service.includes('support') || service.includes('streaming')) {
              // Create a key using the service name
              const key = service.replace(/_/g, ' ');

              // Check if the service is related to Internet
              const serviceValue = categorizeService(churn);

              // Find the corresponding item in the serviceChurnList
              const existingItem = serviceChurnList.find(item => item.service === key && item.churn === serviceValue);

              if (existingItem) {
                  // If the item already exists, increment the amount
                  existingItem.amount += 1;
              } else {
                  // If the item does not exist, create a new item
                  const newItem = {
                      service: key,
                      churn: serviceValue,
                      amount: 1
                  };
                  serviceChurnList.push(newItem);
              }
          }
      }
  });

  return serviceChurnList;
}

// function for second plot (payment method)
function createPaymentChurnList(data) {
  const results = [];

  // Define the payment methods
  const paymentMethods = [
    "Mailed check",
    "Electronic check",
    "Credit card (automatic)",
    "Bank transfer (automatic)"
  ];
  
  // Loop through each payment method
  for (const paymentMethod of paymentMethods) {
    // Count the number of churns (Yes and No) for the current payment method
    const churnYesCount = data.filter(item => item.payment_method === paymentMethod && item.churn === "Yes").length;
    const churnNoCount = data.filter(item => item.payment_method === paymentMethod && item.churn === "No").length;
  
    // Create objects for Yes and No churns and push them to the result list
    results.push({ payment: paymentMethod, churn: "Yes", amount: churnYesCount });
    results.push({ payment: paymentMethod, churn: "No", amount: churnNoCount });
  }

  return results;
  
}

// function for third plot (service)
function generateChurnData(customerList) {
  // Create an object to store data for each year and churn status
  const churnData = {};

  // Iterate through the customer list
  customerList.forEach(customer => {
    // Calculate the year based on tenure
    const year = `Year ${Math.floor((customer.tenure - 1) / 12) + 1}`;

    // Update churn data
    if (!churnData[year]) {
      churnData[year] = {
        Yes: 0,
        No: 0,
      };
    }

    churnData[year][customer.churn]++;
  });

  // Convert object to the desired array format and order by year
  const resultArray = [];
  Object.keys(churnData).sort().forEach(year => {
    for (const churnStatus in churnData[year]) {
      resultArray.push({
        year,
        churn: churnStatus,
        amount: churnData[year][churnStatus],
      });
    }
  });

  return resultArray;
}


// main function containing all three plots
const plotData = async (category = "all") => {
  // fetch data from flask server
  const data = await fetch('http://127.0.0.1:5000/');
  const gendata = await fetch('http://127.0.0.1:5000/generate');


  // convert data to json
  const jsonData = await data.json();
  const jsonGenData = await gendata.json();

  var dataDictArr = []

  jsonData.forEach((item) => {
      dataDictArr.push({
        'customer_ID': item[0],
        'gender': item[1],
        'senior_citizen': item[2],
        'partner': item[3],
        'dependants': item[4],
        'tenure': item[5],
        'phone_service': item[6],
        'multiple_lines': item[7],
        'internet_service': item[8],
        'online_security': item[9],
        'online_backup': item[10],
        'device_protection': item[11],
        'tech_support': item[12],
        'streaming_TV': item[13],
        'streaming_movies': item[14],
        'contract': item[15],
        'paperless_billing': item[16],
        'payment_method': item[17],
        'monthly_charges': item[18],
        'total_charges': item[19],
        'churn': item[20],
      })
  })

  // filter data and return only the category selected
  if (category != 'all') { dataDictArr = dataDictArr.filter(item => item.contract === category) }


  // get data for each plot
  const plot2 = createPaymentChurnList(dataDictArr);
  const plot3 = createServiceChurnList(dataDictArr);
  const plot4 = generateChurnData(dataDictArr);

  ////////////////////////////////
  //        PLOTS
  ////////////////////////////////
  const plotBar = Plot.plot({
    marginBottom: 100,
    fx: {padding: 0, label: null, tickRotate: 90, tickSize: 6},
    x: {axis: null, paddingOuter: 0.2},
    y: {grid: true},
    color: {legend: true},
    marks: [
      Plot.barY(dataDictArr, Plot.groupX({y2: "count"}, {x: "churn", fx: "gender", fill: "churn"})),
      Plot.ruleY([0])
    ]
  })

  // insert into html
  const barDiv = document.querySelector("#plot1");
  barDiv.innerHTML = ''
  barDiv.append(plotBar);

  const plotBar2 = Plot.plot({
    x: {axis: null},
    y: {tickFormat: "s", grid: true},
    color: {scheme: "blues", legend: true},
    marks: [
      Plot.barY(plot2, {
        x: "churn",
        y: "amount",
        fill: "churn",
        fx: "payment",
      }),
      Plot.ruleY([0])
    ]
  })

  // insert into html
  const barDiv2 = document.querySelector("#plot2");
  barDiv2.innerHTML = ''
  barDiv2.append(plotBar2);

  const plotBar3 = Plot.plot({
    x: {axis: null},
    y: {tickFormat: "s", grid: true},
    color: {scheme: "reds", legend: true},
    marks: [
      Plot.barY(plot3, {
        x: "churn",
        y: "amount",
        fill: "churn",
        fx: "service",
      }),
      Plot.ruleY([0])
    ]
  })

  // insert into html
  const barDiv3 = document.querySelector("#plot3");
  barDiv3.innerHTML = ''
  barDiv3.append(plotBar3);

  const plotBar4 = Plot.plot({
    x: {axis: null},
    y: {tickFormat: "s", grid: true},
    color: {scheme: "greens", legend: true},
    marks: [
      Plot.barY(plot4, {
        x: "churn",
        y: "amount",
        fill: "churn",
        fx: "year",
      }),
      Plot.ruleY([0])
    ]
  })

  // insert into html
  const barDiv4 = document.querySelector("#plot4");
  barDiv4.innerHTML = ''
  barDiv4.append(plotBar4);

  ////////////////////////////////
  //        Table
  ////////////////////////////////

  var totalCustomers = dataDictArr.length;

  // Calculate the percentage of customers with churn value "No"
  var churnNoCount = dataDictArr.filter(customer => customer.churn === 'No').length;
  var churnNoPercentage = ((churnNoCount / totalCustomers) * 100).toFixed(2) + '%';

  // calculate the percentage of customers with churn value "No" from the generated data combined with the original data
  var churnNoCountGen = jsonGenData.filter(customer => customer.churn === 'No').length;
  var churnNoPercentageGen = ((churnNoCountGen / totalCustomers) * 100).toFixed(2) + '%';
  // add percentages of churnNoPercentage into churnNoPercentageGen together
  churnNoPercentageGen = (parseFloat(churnNoPercentageGen) + parseFloat(churnNoPercentage)).toFixed(2) + '%' + '(' + churnNoPercentageGen + ')';

  // Calculate the total revenue
  var totalRevenue = dataDictArr.reduce((total, customer) => total + customer.total_charges, 0).toFixed(2);

  // Calculate the total revenue from the generated data combined with the original data
  var totalRevenueGen = jsonGenData.reduce((total, customer) => total + customer.total_charges, 0).toFixed(2);

  // Calculate the percentage differnce between the total revenue from the generated data combined with the original data and the original data
  var percentageChange = (totalRevenueGen * 100 / totalRevenue);

  // Get the table row to update
  var tableRow = document.getElementById('attrition-table-body').getElementsByTagName('tr')[0];

  // Update the cells with the calculated values
  tableRow.cells[0].textContent = totalCustomers;
  tableRow.cells[1].textContent = churnNoPercentage;
  tableRow.cells[2].textContent = churnNoPercentageGen;
  tableRow.cells[3].textContent = '$' + totalRevenue;
  tableRow.cells[4].textContent = percentageChange.toFixed(2) + '%';
  tableRow.cells[5].textContent = '$' + totalRevenueGen;

}

await plotData()