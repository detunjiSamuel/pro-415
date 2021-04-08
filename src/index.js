console.log("still works");

let chart = document.getElementById("myChart");
let countries = {};

d3.csv("obesity-cleaned.csv", function(data){
    getCountries(data)
});


function getCountries(data)
{
    console.log("action : get countries");
    for(let i = 0 ; i <data.length ;i++)
    {
        //add countries
        current =  data[i].Country;
        if(countries[current])
        {
            countries[current]+=1;
            continue;
        }
        countries[current]=0;
    }
    localStorage.setItem('countries',countries );
}