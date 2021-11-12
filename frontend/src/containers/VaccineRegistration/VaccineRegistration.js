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
      timeSlotSelected: "", 
      timeSlots: [], 
      alertOpen: false
    };
    this.handleSelect = this.handleSelect.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.getVaccineCenter = this.getVaccineCenter.bind(this);
    this.handleNRICChange = this.handleNRICChange.bind(this); 
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleNameChange = this.handleNameChange.bind(this);
    this.handleClickOpen = this.handleClickOpen.bind(this); 
    this.handleClose = this.handleClose.bind(this);
  }

  getVaccineCenter() {
    axios.get(`http://localhost:8000/bookings/vaccine_centers`)
    .then(res=>{
      if(res.data.success){
        this.setState({...this.state, allCenters: res.data.data})
      }
    })
  }

  componentDidMount(){
    this.getVaccineCenter()    
  }

  handleSelect(event) {
    const state = this.state;
    this.setState({...state, selectedCenter: event.target.value});
  }
  handleDateChange(value) {
    const state = this.state;
    this.setState({...state, date: value});
  }
  handleNameChange(event) {
    this.setState({...this.state, name: event.target.value})
  }
  handleNRICChange(event) {
    this.setState({...this.state, NRIC: event.target.value})
  }
  handleSubmit() {
    let data = {
      "NRIC": this.state.NRIC, 
      "name": this.state.name, 
      "centerId": this.state.selectedCenter, 
      "timeSlot": this.state.date
    }
    axios.post('http://localhost:8000/bookings/add', data )
    .then(res => {
      if (res.data.success) {
        this.handleClickOpen()
      }
    })
  }

  handleClickOpen() {
    this.setState({...this.state, alertOpen: true});
  };

  handleClose(){
    this.setState({...this.state, alertOpen: false});
  };
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
            <DateTimePicker
              renderInput={(props) => <TextField {...props} />}
              label="Slot"
              value={this.state.date}
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
        <Dialog
        open={this.state.alertOpen}
        onClose={this.handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
            Success
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Registration Successful!
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
