import { Component, ChangeDetectorRef, signal, OnChanges } from '@angular/core';
import { SubnetCalcService } from 'src/app/services/subnet-calc.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'angular_api_portal';
  // Consturctor
  constructor(private cdr: ChangeDetectorRef, private subCalc: SubnetCalcService) { }

  // Variables configured for much more complex and detailed calculator than in the Demo Repository.
  IPAddress: any;
  subnetIP: any;
  enteredIP = signal<boolean>(false);
  cidrSelected = signal<boolean>(false);
  subnetSelected: any;
  subnetCList = signal<string[]>([]);
  dataIsLoading: boolean = false;
  numHosts: any;
  showIPList: boolean = true;
  disableIPList: boolean = false;


  // API Response Variables
  APIResponse: any;
  displayedColumns = ["N", "B", "F", "L", "S", "H", "NH"];
  returnedData: any;
  sendData = {};
  subnetList: string[] = [];
  returnListPresent: boolean = false;
  rows: any;

  
  ngOnInit(): void {
    // Initialization goes here.
    // Obtain Auth when needed for DB or API calls here.
  }

  selected($event: OnChanges) {
    this.cidrSelected.update(value => true)
    this.subnetSelected = $event
    if (+this.subnetSelected < 16) {
      this.showIPList = false
      this.disableIPList = true
    }

  }
  onToggle() {
    this.dataIsLoading = !this.dataIsLoading
  }
  onPress() {
    this.dataIsLoading = true
    this.sendData = {
      "ip": this.IPAddress,
      "hosts": this.numHosts
    }
    this.subCalc.subnetAPI(this.sendData).subscribe(
      data => {
        this.APIResponse = data
        this.returnedData = JSON.parse(this.APIResponse)
        this.rows = Object.values(this.returnedData)
        this.returnListPresent = true
        this.dataIsLoading = false
        // Need to add error handling in the API response.
      }
    )
  }

  IPValidator(newVal: string) {
    // Allow only IP address to be entered into input field.
    let dec = 3
    let justDigits = newVal.replace(/[^0-9\.]/, '')
    this.IPAddress = null;
    this.cdr.detectChanges();
    this.IPAddress = justDigits;
    let parser = this.IPAddress.split(".")
    if (this.IPAddress.includes("..")) {
      this.IPAddress = this.IPAddress.slice(0, -1)
    }
    if (this.IPAddress[0] === "0" || this.IPAddress[0] === "." || this.IPAddress === ".." || this.IPAddress === ",") {
      this.IPAddress = this.IPAddress.slice(0, -1)
    }
    if (parser[dec - 2] === "00" || parser[dec - 1] === "00" || parser[dec] === "00") {
      this.IPAddress = this.IPAddress.slice(0, -1)
    }
    if (!this.IPAddress.includes(".") && this.IPAddress.includes(",") || this.IPAddress.includes(",,")) {
      this.IPAddress = this.IPAddress.slice(0, -1)
    }
    try {
      if (this.IPAddress.match(/\./g).length < dec && this.IPAddress.includes(",")) {
        this.IPAddress = this.IPAddress.slice(0, -1)
      }
      if (this.IPAddress.match(/\./g).length > 3) {
        this.IPAddress = this.IPAddress.slice(0, -1)
      }
      if (this.IPAddress.match(/\./g).length === dec) {
        if (this.IPAddress.includes(",")) {
          this.IPAddress = this.IPAddress + " "
        }
        else if (this.IPAddress.match(/\./g).length > 3) {
          this.IPAddress = this.IPAddress.slice(0, -1)
        }
        else if (parser[0] === "00" || parser[1] === "00" || parser[2] === "00" || parser[3] === "00") {
          this.IPAddress = this.IPAddress.slice(0, -1)
        }
      }
    } catch (error) { }
    if (+parser[0] > 255 || +parser[1] > 255 || +parser[2] > 255 || +parser[3] > 255) {
      this.IPAddress = this.IPAddress.slice(0, -1)
    }
    this.enteredIP.update(value => true)
  }
}
