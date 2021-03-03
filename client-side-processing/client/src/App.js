import { Fragment, useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { Container, Row, Col } from "react-bootstrap";
import HeatMap from "./components/HeatMap";

const App = () => {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const sdk_res = await axios.get("http://localhost:5000/sdk");
      const app_res = await axios.get("http://localhost:5000/app");
      const sdkapp_res = await axios.get("http://localhost:5000/appsdk");

      setData({
        sdk: sdk_res.data,
        app: app_res.data,
        sdkapp: sdkapp_res.data,
      });
    };

    fetchData().then(function () {
      setLoading(false);
    });
  }, []);

  return (
    <Fragment>
      <Container>
        <Row className="d-flex row justify-content-center align-self-center">
          {loading ? (
            <Row>
              <Col className="d-flex row justify-content-center align-self-center row text-center">
                <h1 className="align-middle">Loading...</h1>
              </Col>
            </Row>
          ) : (
            <HeatMap data={data} />
          )}
        </Row>
      </Container>
    </Fragment>
  );
};

export default App;
