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
  Dialog, 
  DialogActions, 
  DialogContent, 
  DialogContentText, 
  DialogTitle
} from "@mui/material";
import DatePicker from "@mui/lab/DatePicker";
import React, { Component } from "react";
import axios from 'axios';

export class EditVaccineRegistration extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedCenter: 0,
      date: new Date(),
      allCenters: [], 
      NRIC: "", 
      name: "", 
      timeSlotSelected: "default", 
      timeSlots: [], 
      alertOpen: false, 
      dialogTitle:"", 
      dialogContent:"", 
      id: 0, 
      originalDate: new Date(), 
      originalCenter: 0, 
      originalTimeSlot: "default"
    };
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.getVaccineCenter = this.getVaccineCenter.bind(this);
    this.getBooking = this.getBooking.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getAvailableSlot = this.getAvailableSlot.bind(this);
    this.handleSelectTimeSlot = this.handleSelectTimeSlot.bind(this);
    this.handleClickOpen = this.handleClickOpen.bind(this); 
    this.handleClose = this.handleClose.bind(this);
  }

  handleSelectTimeSlot(event){
    this.setState({...this.state, timeSlotSelected: event.target.value});
  }
  
  getAvailableSlot() {
    let myDate = this.state.date.toISOString().split('T')[0]
    console.log(`http://localhost:8000/bookings/time_slots?date=${myDate}&center_id=${this.state.selectedCenter} `)
    axios.get(`http://localhost:8000/bookings/time_slots?date=${myDate}&center_id=${this.state.selectedCenter}`).then(res => {
      console.log(res.data)
      this.setState({...this.state, timeSlots: res.data.data})
    }).catch(e => 
      {
        console.log("test",e.response )
        // TODO: vaccination empty  
      })
  }

  getBooking(bookingId){
    axios.get(`http://localhost:8000/bookings/${bookingId}`)
    .then(res=>{
      if(res.data.success){
        let received_data = res.data.data
        console.log(received_data.timeSlot)
        this.setState({
          ...this.state, 
          id: received_data.id, 
          NRIC: received_data.NRIC, 
          name: received_data.name, 
          selectedCenter: received_data.centerId, 
          date: new Date(received_data.startTime),
          originalDate: new Date(received_data.startTime),  
          originalCenter: received_data.centerId, 
          timeSlotSelected: received_data.timeSlot,
          originalTimeSlot: received_data.timeSlot
        })
        this.getAvailableSlot();
      }
    })

  }

  getVaccineCenter() {
    axios.get(`http://localhost:8000/bookings/vaccine_centers`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, allCenters: res.data.data})
        this.getAvailableSlot()
      }
    })
  }

  componentDidMount(){
    this.getVaccineCenter()    
    this.getBooking(this.props.match.params.bookingId)
  }
  
  handleSelect(event) {
    let selectedCenterId = event.target.value
    this.setState({...this.state, selectedCenter: selectedCenterId});
    this.getAvailableSlot();
  }
  handleDateChange(value) {
    const state = this.state;
    this.setState({ ...state, date: value});
    this.getAvailableSlot();
  }

  handleClickOpen(title, content) {
    this.setState({...this.state, alertOpen: true, dialogTitle: title, dialogContent: content});
  };

  handleClose(){
    this.setState({...this.state, alertOpen: false,dialogTitle: "", dialogContent: ""});
  };

  handleSubmit(event) {
    if (!(this.state.originalCenter === this.state.selectedCenter && this.state.originalTimeSlot === this.state.timeSlotSelected && this.state.date.toISOString().split('T')[0] === this.state.originalDate.toISOString().split('T')[0] )){
      let data = {
        // "NRIC": this.state.NRIC, 
        // "name": this.state.name, 
        "centerId": this.state.selectedCenter, 
        "date": this.state.date.toISOString().split('T')[0], 
        "time_slot": this.state.timeSlotSelected
      }
      axios.put(`http://localhost:8000/bookings/${this.state.id}/`, data)
      .then(res=>{
        if(res.data.success){
          this.handleClickOpen("Success", "Updated " + JSON.stringify(res.data.data))
          this.getBooking(this.props.match.params.bookingId)
        }
      }).catch(err => console.log(err.response.data.error))
    }
    else {
      this.handleClickOpen("No Changes", "No changes made")
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
              value={this.state.NRIC}
              sx={{mb: 2}}
              autoFocus
              disabled
            />
            <TextField
              required
              fullWidth
              id="name"
              label="Full Name"
              value={this.state.name}
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
              value={this.state.selectedCenter || 1}
              onChange={this.handleSelect}
              sx={{mb: 2}}
              defaultValue = "" 
            >
              {this.state.allCenters.map((v) => {
                return (
                  <MenuItem key={v.id} value={v.id}>
                    {v.name}
                  </MenuItem>
                );
              })}
            </Select>
            <DatePicker
              renderInput={(props) => <TextField {...props} />}
              label="Slot"
              value={this.state.date || new Date()}
              onChange={this.handleDateChange}
              required
            />
            <InputLabel id="slotAvailableLabel">Time Slot</InputLabel>
            <Select
              labelId="slotAvailable"
              label="Time Slot"
              required
              fullWidth
              id="timeSlot"
              value={this.state.timeSlots.find(data => {
                return data[0] === this.state.timeSlotSelected
              }) ? this.state.timeSlotSelected :'default' }
              onChange={this.handleSelectTimeSlot}
              description="Please select time slot"
              sx={{mb: 2}}
            >
              {console.log(`selected`, this.state.timeSlotSelected)}
              <MenuItem key={"default"} value={"default"} disabled>{"Please select time slot"}</MenuItem>;
              {this.state.timeSlots.map((v) => {
                return <MenuItem key={v[0]} value={v[0]}>{v[1]}</MenuItem>;
              })}
            </Select>
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
        {/* add dialog */}

        <Dialog
          open={this.state.alertOpen}
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
              {this.state.dialogTitle}
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {this.state.dialogContent}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} autoFocus>
              Close
            </Button>
          </DialogActions>
        </Dialog>

      </React.Fragment>
    );
  }
}
