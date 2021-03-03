import React, { useEffect, useState, Fragment } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import * as d3 from "d3";
import { processData } from "../process";

const HeatMap = ({ data }) => {
  const { sdk, sdkapp } = data;

  //Holds the state of the current visualization type (absolute/percentage)
  const [perc, setPerc] = useState(0);

  //Set initial view
  const [selectedSDKs, setSelectedSDKs] = useState(
    sdk.map((sdk_iter) =>
      sdk_iter.name == "PayPal" ||
      sdk_iter.name == "Stripe" ||
      sdk_iter.name == "Braintree"
        ? sdk_iter.id
        : null
    )
  );

  const [displayApps, setDisplayApps] = useState();

  //Re-render if dataset or visualization type changes
  useEffect(() => {
    d3.selectAll("svg").remove();

    //Processes the current dataset and gives back an array for d3
    const dataset = processData(sdk, selectedSDKs, sdkapp);

    const margin = { top: 80, right: 25, bottom: 30, left: 150 },
      width = 950 - margin.left - margin.right,
      height = 950 - margin.top - margin.bottom;

    //Create an svg for d3
    if (dataset) {
      const svg = d3
        .select("#svg")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      //Labels of rows and columns -> unique identifier of the column called 'to_name' and 'from_name'
      const to = d3.map(dataset, function (d) {
        return d.to_name;
      });

      const from = d3.map(dataset, function (d) {
        return d.from_name;
      });

      //Build X scales and axis:
      const x = d3.scaleBand().range([0, width]).domain(to).padding(0.05);
      svg
        .append("g")
        .style("font-size", 8)
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain")
        .remove();

      //Build Y scales and axis:
      const y = d3.scaleBand().range([height, 0]).domain(from).padding(0.05);
      svg
        .append("g")
        .style("font-size", 8)
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain")
        .remove();

      //Build color scale
      var myColor = d3
        .scaleLinear()
        .range(["#cee2de", "#4aa996"])
        .domain([1, 300]);

      //Hover/Move/Leave a cell
      const mouseover = function (e) {
        d3.select(e.target).style("stroke", "black").style("opacity", 1);
      };
      const mousemove = function (e) {};
      const mouseleave = function (e) {
        d3.select(e.target).style("stroke", "none").style("opacity", 0.8);
      };

      //Add the squares
      const g = svg
        .selectAll()
        .data(dataset, function (d) {
          return d.to_name + ":" + d.from_name;
        })
        .enter()
        .append("g")
        .on("click", function (d) {
          setDisplayApps(d.to_name, d.from_name);
          console.log(displayApps);
        });

      //Build the rectangles
      g.append("rect")
        .attr("x", function (d) {
          return x(d.to_name);
        })
        .attr("y", function (d) {
          return y(d.from_name);
        })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function (d) {
          return myColor(d.value);
        })
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
        .on("mouseover", (e) => mouseover(e))
        .on("mousemove", (e) => mousemove(e))
        .on("mouseleave", (e) => mouseleave(e));

      //Add text inside rects
      g.append("text")
        .style("fill", "black")
        .text(function (d) {
          //If absolute is selected return the value
          if (perc == 0) {
            return d.value;
          } else {
            //Else normalize by row and return percentage
            let sum = 0;

            dataset.forEach(function (appsdk) {
              if (appsdk.from_id == d.from_id) {
                sum += appsdk.value;
              }
            });
            return Math.round((d.value * 100) / sum) + "%";
          }
        })
        .attr("x", function (d) {
          return x(d.to_name);
        })
        .attr("y", function (d) {
          return y(d.from_name);
        })
        .attr("dx", x.bandwidth() / 2)
        .attr("dy", y.bandwidth() / 2)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central");
    }
  }, [selectedSDKs, perc]);

  return (
    <Fragment>
      <Col xs={10}>
        <div id="svg" />
      </Col>
      <Col className="d-flex row justify-content-center align-self-center">
        <h4 className="font-weight-bold">SDKs</h4>
        <form className="mb-5">
          {sdk.map(function (sdk_iter) {
            return (
              <>
                <input
                  type="checkbox"
                  checked={selectedSDKs.includes(sdk_iter.id) ? true : false}
                  id={sdk_iter.id}
                  name={sdk_iter.id}
                  value={sdk_iter.id}
                  onClick={() => {
                    //Check if sdk is already selected, if not add it to the selection else remove it
                    selectedSDKs.includes(sdk_iter.id)
                      ? setSelectedSDKs(
                          selectedSDKs.filter(
                            (checked) => checked != sdk_iter.id
                          )
                        )
                      : setSelectedSDKs((selectedSDKs) => [
                          ...selectedSDKs,
                          sdk_iter.id,
                        ]);
                  }}
                ></input>
                <label for={sdk_iter.id} class="mr-1">
                  {sdk_iter.name}
                </label>
                <br></br>
              </>
            );
          })}
        </form>
        <br />
        <br />
        <h3 className="font-weight-bold">Values</h3>
        <Button variant="primary" onClick={() => setPerc(!perc)}>
          Absolute/Percentage
        </Button>
      </Col>
      <Row>
        <Col>{displayApps}</Col>
      </Row>
    </Fragment>
  );
};

export default HeatMap;
