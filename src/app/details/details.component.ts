import { Component, Input, OnInit } from "@angular/core";
import { DataService } from "../data.service";
import { Laptop } from "../laptop";
import { HomeComponent } from "../home/home.component";
import { moveIn, fallIn } from "../routing.animations";

import { HttpClient } from 'selenium-webdriver/http';
import { HttpResponse } from '@angular/common/http';
import { FormsModule, NgForm } from '@angular/forms';
import { NgModule } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import {Observable} from 'rxjs';
import { keyValuesToMap } from '@angular/flex-layout/extended/typings/style/style-transforms';


@Component({
  selector: "app-details",
  templateUrl: "./details.component.html",
  styleUrls: ["./details.component.scss"],
  animations: [moveIn(), fallIn()],
  host: { "[@moveIn]": "" }
})
export class DetailsComponent implements OnInit {

  asin;
  brandName: string;
  laptops: Laptop[] = [];
  item: Laptop;

  constructor(private one_detail: DataService,
              private route: ActivatedRoute,
              private homeFeatures: HomeComponent) {
  }


  ngOnInit() {
    this.asin = this.route.snapshot.params['asin'];
    this.showDetails()
  }

  showDetails() {
    this.one_detail.getLaptop_details(this.asin).subscribe(data => {
      this.item = data[0];
      // console.log(this.item.imagePath);
    });
  }

  sendItem(){
    let laptop = "{";
    const mapped = Object.keys(this.item).map(key => ({ type: key, value: this.item[key] }));
    for(let i in mapped){
      if (mapped[i]['type'] == 'asin' || mapped[i]['type'] == 'productTitle'){
        continue;
      }
      if (mapped[i]['type'] == 'price') {
        laptop = laptop + '"' + mapped[i]['type'] + '"';
        laptop += ' :{';
        laptop += '"' + 'value' + '"';
        laptop += ':' + '"' + mapped[i]['value'] + '"';
        laptop += ', ';
        laptop += '"weight" : 1 },'
      } 
      laptop = laptop + '"' +mapped[i]['type'] + '"'; 
      laptop += ' :{';
      laptop += '"' + mapped[i]['type'] + 'Value' + '"';
      laptop += ':' + '"' + mapped[i]['value'] + '"';
      laptop += ', ';
      laptop += '"weight" : 1 },'
    }
    laptop = laptop.substring(0, laptop.length - 1);
    laptop += "}";
    // console.log(laptop);
    laptop = JSON.parse(JSON.stringify(laptop));
    console.log(laptop);
    this.one_detail.setLaptop(laptop).subscribe(data=>console.log(data));
  }

  sendLaptops(){
    this.one_detail.getCritizedResult();
  }
}
