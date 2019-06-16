import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { DetailsComponent } from "./details/details.component";
import { CartComponent } from "./cart/cart.component";
import {SearchComponent} from "./search/search.component";

const routes: Routes = [
  { path: "", component: HomeComponent },
  { path: "details", component: DetailsComponent },
  { path: "cart", component: CartComponent },
   {path: "home", component:HomeComponent},
  {path: "search", component:SearchComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
