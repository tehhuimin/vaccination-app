import {
  Table,
  Box,
  Button,
  CssBaseline,
  Typography,
  TableContainer,
  TableCell,
  TableBody,
  TableRow,
  TableHead,
  Container,
} from "@mui/material";
import { Link } from 'react-router-dom';
import ModeEditIcon from "@mui/icons-material/ModeEdit";
import DeleteIcon from "@mui/icons-material/Delete";
import React, { useEffect, useState } from "react";
import axios from 'axios';

export function VaccineRegistrationListing () {
  const [bookings, setBookings] = useState([])
  const [timeSlots, setTimeSlots] = useState([])

  useEffect(()=>{
    getBookings()
    getTimeSlots()
  }, [])

  const getBookings = () => {
    axios.get(`http://localhost:8000/bookings`)
    .then(res=>{
      if(res.data.success){
        setBookings(res.data.data)
      }
    })
  }

  const getTimeSlots = () => {
    axios.get(`http://localhost:8000/bookings/time_slots`)
    .then(res=>{
      if(res.data.success){
        setTimeSlots(res.data.data)
      }
    })
  }

  const deleteBooking = (bookingId) => {
    axios.delete(`http://localhost:8000/bookings/${bookingId}/`)
    .then(res=>{
      if(res.data.success){
        getBookings()
      }
    })
      
  }

  return (
      <React.Fragment>
        <CssBaseline />
        <Container>
          <Box sx={{mt: 8}}>
            <Typography component="h1" variant="h5">
              Active Booking
            </Typography>
            <TableContainer component={Box}>
              <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell align="left">Center Name</TableCell>
                    <TableCell align="left">Time Slot</TableCell>
                    <TableCell align="left">&nbsp;</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {console.log(bookings)}
                  {bookings.map((row) => (
                    <TableRow
                      key={row.id}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">
                        {row.name}
                      </TableCell>
                      <TableCell align="left">{row.centerName}</TableCell>
                      <TableCell align="left">
                        {row.startTime + " " + timeSlots.find(slot => slot[0] ===row.timeSlot)[1]}
                        {/* {new Date(row.startTime).toString()} */}
                      </TableCell>
                      <TableCell align="left">
                        <Button component={Link} to={`/bookings/${row.id}`}>
                          <ModeEditIcon />
                        </Button>
                        <Button onClick={()=> deleteBooking(row.id)}>
                          <DeleteIcon />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </Container>
      </React.Fragment>
    );
  }

