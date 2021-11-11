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
      edited: false, 
      vaccineCenters: [], 
      booking: {
        "id": 0,
        "name": "", 
        "NRIC": "",
        "selectedCenter": 0, 
        "centerName": "",
        "date": new Date()
      }
    };
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.getVaccineCenter = this.getVaccineCenter.bind(this);
    this.getBooking = this.getBooking.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  
  getBooking(bookingId){
    axios.get(`http://localhost:8000/bookings/${bookingId}`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, booking: res.data.data , edited: false })
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
    let selectedCenterId = event.target.value
    let selectedCenterName = this.state.vaccineCenters.find(center => center.id === selectedCenterId)?.name || ''
    this.setState({
      ...this.state, 
      edited: true, 
      booking: {
        ...this.state.booking, 
        centerId: selectedCenterId, 
        centerName: selectedCenterName
    }});
  }
  handleDateChange(value) {
    const state = this.state;
    this.setState({ ...state, edited: true, booking: {...this.state.booking, date: value}});
  }
  handleSubmit(event) {
    if (this.state.edited){
      let data = this.state.booking
      axios.put(`http://localhost:8000/bookings/${this.state.booking.id}/`, data)
      .then(res=>{
        if(res.data.success){
          console.log("Success")
          this.getBooking(this.props.match.params.bookingId)
        }
      })
    }
    else {
      console.log("no changes made")
    }
    
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
              value={this.state.booking.NRIC}
              sx={{mb: 2}}
              autoFocus
              disabled
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
              disabled
            />
            <InputLabel id="vaccineCenterLabel">Vaccine Center</InputLabel>
            <Select
              labelId="vaccineCenterLabel"
              label="Vaccine Center"
              required
              fullWidth
              id="vaccineCenter"
              value={this.state.booking.centerId || 1}
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
              value={this.state.booking.date || new Date()}
              onChange={this.handleDateChange}
              required
            />
            <Button
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={this.handleSubmit}
            >
              Register!
            </Button>
          </Box>
        </Container>
      </React.Fragment>
    );
  }
}
