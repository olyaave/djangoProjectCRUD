import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';    // add this
import { FormsModule } from '@angular/forms';    // add this
import { AppComponent } from './app.component';
import { UserService } from './user.service';
import {BlogPostService} from "./blog_post.service";    // add this

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, FormsModule, HttpClientModule],    // add this
  providers: [UserService, BlogPostService],    // add this
  bootstrap: [AppComponent]
})
export class AppModule { }
