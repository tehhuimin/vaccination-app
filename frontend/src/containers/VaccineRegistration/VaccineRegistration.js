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
import DatePicker from '@mui/lab/DatePicker';
import React, { Component } from "react";
import axios from 'axios';

export class VaccineRegistration extends Component {
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
      dialogContent:""
    };
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.getVaccineCenter = this.getVaccineCenter.bind(this);
    this.handleNRICChange = this.handleNRICChange.bind(this); 
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleNameChange = this.handleNameChange.bind(this);
    this.handleClickOpen = this.handleClickOpen.bind(this); 
    this.handleClose = this.handleClose.bind(this);
    this.getAvailableSlot = this.getAvailableSlot.bind(this);
    this.handleSelectTimeSlot = this.handleSelectTimeSlot.bind(this);
  }

  getVaccineCenter() {
    axios.get(`http://localhost:8000/bookings/vaccine_centers`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, allCenters: res.data.data, selectedCenter:res.data.data[0]?.id || 1 })
        this.getAvailableSlot()
      }
    })
  }

  getAvailableSlot() {
    let myDate = this.state.date.toISOString().split('T')[0]
    console.log(`http://localhost:8000/bookings/time_slots?date=${myDate}&center_id=${this.state.selectedCenter} `)
    axios.get(`http://localhost:8000/bookings/time_slots?date=${myDate}&center_id=${this.state.selectedCenter}`).then(res => {
      console.log(res.data)
      this.setState({...this.state, timeSlots: res.data.data})
    }).catch(e => 
      {
        this.setState({...this.state, alertOpen: true, dialogTitle: "Error", dialogContent: e.response.data.error || ''});
      })
  }

  componentDidMount(){
    this.getVaccineCenter()    
  }

  handleSelect(event) {
    const state = this.state;
    this.setState({...state, selectedCenter: event.target.value});
    this.getAvailableSlot();
  }
  handleDateChange(value) {
    const state = this.state;
    this.setState({...state, date: value});
    this.getAvailableSlot();
  }
  handleNameChange(event) {
    this.setState({...this.state, name: event.target.value})
  }
  handleNRICChange(event) {
    this.setState({...this.state, NRIC: event.target.value})
  }
  handleSubmit() {
    const regexNRIC = new RegExp('^[a-zA-Z][0-9]{7}[a-zA-Z]$', 'g');
    if (this.state.NRIC === "" || this.state.NRIC === null || this.state.NRIC === undefined ) {
      return this.handleClickOpen("Error", "Please fill in NRIC")
    }
    if (!regexNRIC.test(this.state.NRIC)){
      return this.handleClickOpen("Error", "NRIC is incorrect")
    }
    if (this.state.name === "" || this.state.name === null || this.state.name === undefined) {
      return this.handleClickOpen("Error", "Please fill in name")
    }
    if (this.state.selectedCenter === null || this.state.selectedCenter === undefined) {
      return this.handleClickOpen("Error", "Please select Vaccination Center")
    }
    if (this.state.date === "" || this.state.date === null || this.state.date === undefined) {
      return this.handleClickOpen("Error", "Please select date")
    }
    if (this.state.timeSlotSelected === "default" || this.state.timeSlotSelected === null || this.state.timeSlotSelected === undefined) {
      return this.handleClickOpen("Error", "Please select time slot")
    }

    let data = {
      "NRIC": this.state.NRIC, 
      "name": this.state.name, 
      "centerId": this.state.selectedCenter, 
      "date": this.state.date.toISOString().split('T')[0], 
      "time_slot": this.state.timeSlotSelected
    }
    axios.post('http://localhost:8000/bookings/add', data )
    .then(res => {
      console.log(res)
      if (res.data.success) {
        let title = "Successful"
        let content = `Created ${JSON.stringify(res.data.data)}`
        this.handleClickOpen(title, content)
      }
    }).catch(e=> {
      this.handleClickOpen("Error", e.response.data.error)
    })
  }

  handleClickOpen(title, content) {
    this.setState({...this.state, alertOpen: true, dialogTitle: title, dialogContent: content});
  };

  handleClose(){
    this.setState({...this.state, alertOpen: false,dialogTitle: "", dialogContent: ""});
  };

  handleSelectTimeSlot(event){
    this.setState({...this.state, timeSlotSelected: event.target.value});
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
              sx={{mb: 2}}
              onChange={this.handleNRICChange}
              autoFocus
            />
            <TextField
              required
              fullWidth
              id="name"
              label="Full Name"
              name="name"
              autoComplete="name"
              onChange={this.handleNameChange}
              sx={{mb: 2}}
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
            >
              {this.state.allCenters.map((v) => {
                return <MenuItem key={v.id} value={v.id}>{v.name}</MenuItem>;
              })}
            </Select>
            <DatePicker
              renderInput={(props) => <TextField {...props} />}
              label="Slot"
              value={this.state.date}
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
              value={this.state.timeSlotSelected || 'default'}
              onChange={this.handleSelectTimeSlot}
              description="Please select time slot"
              sx={{mb: 2}}
            >
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
