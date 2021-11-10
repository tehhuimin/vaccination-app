import {
  Container,
  Box,
  Button,
  Typography,
  CssBaseline,
  TextField,
  Select,
  MenuItem,
  InputLabel,
} from "@mui/material";
import DateTimePicker from "@mui/lab/DateTimePicker";
import React, { Component } from "react";
import axios from 'axios';

export class EditVaccineRegistration extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCenter: 0, 
      date: new Date(),
      vaccineCenters: [], 
      booking: {
        "id": 0,
        "name": "", 
      }
    };
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.getVaccineCenter = this.getVaccineCenter.bind(this);
    this.getBooking = this.getBooking.bind(this);
  }
  
  getBooking(bookingId){
    axios.get(`http://localhost:8000/bookings/${bookingId}`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, date: new Date(res.data.data.startTime), selectedCenter:res.data.data.centerId, booking: res.data.data  })
      }
    })
  }

  getVaccineCenter() {
    axios.get(`http://localhost:8000/bookings/vaccine_centers`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, vaccineCenters: res.data.data})
      }
    })
  }

  componentDidMount(){
    this.getVaccineCenter()    
    this.getBooking(this.props.match.params.bookingId)
  }
  
  handleSelect(event) {
    this.setState({ selectedCenter: event.target.value });
  }
  handleDateChange(value) {
    const state = this.state;
    this.setState({ ...state, date: value });
  }
  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <Container>
          <Box
            component="form"
            sx={{
              mt: 8,
            }}
          >
            <Typography component="h1" variant="h5">
              Book a slot
            </Typography>
            <TextField
              margin="normal"
              required
              fullWidth
              id="nric"
              label="NRIC Number"
              name="NRIC"
              autoComplete="nric"
              value={this.state.booking.id}
              sx={{mb: 2}}
              autoFocus
            />
            <TextField
              required
              fullWidth
              id="name"
              label="Full Name"
              value={this.state.booking.name}
              sx={{mb: 2}}
              name="name"
              autoComplete="name"
            />
            <InputLabel id="vaccineCenterLabel">Vaccine Center</InputLabel>
            <Select
              labelId="vaccineCenterLabel"
              label="Vaccine Center"
              required
              fullWidth
              id="vaccineCenter"
              value={this.state.selectedCenter}
              onChange={this.handleSelect}
              sx={{mb: 2}}
              defaultValue = "" 
            >
              {this.state.vaccineCenters.map((v) => {
                return (
                  <MenuItem key={v.id} value={v.id}>
                    {v.name}
                  </MenuItem>
                );
              })}
            </Select>
            <DateTimePicker
              renderInput={(props) => <TextField {...props} />}
              label="Slot"
              value={this.state.date}
              onChange={this.handleDateChange}
              required
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Register!
            </Button>
          </Box>
        </Container>
      </React.Fragment>
    );
  }
}
