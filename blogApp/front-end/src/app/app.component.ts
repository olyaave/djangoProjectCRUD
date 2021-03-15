import {Component, OnInit} from '@angular/core';
import {UserService} from './user.service';
import {BlogPostService} from './blog.service';
import {throwError} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  public user: any;

  public posts: any;

  public new_post: any;

  constructor(private _blogPostService: BlogPostService, public _userService: UserService) { }

  ngOnInit() {
    this.getPosts();
    this.new_post = {};
    this._userService.check();
    this.user = {
      email: '',
      password: ''
    };
  }

  login() {
    this._userService.login({'email': this.user.email, 'password': this.user.password});
  }

   registration() {
    this._userService.registration({'email': this.user.email, 'username': this.user.username, 'password': this.user.password});
  }

  toLogin(){
    this._userService.toLogin();
  }

  toRegistration(){
    this._userService.toRegistration();
  }

  refreshToken() {
    this._userService.refreshToken();
  }

  logout() {
    this._userService.logout();
  }

  getPosts() {
    this._blogPostService.list().subscribe(
      // the first argument is a function which runs on success
      (data) => {
        if('posts' in data)
          this.posts = data['posts'];

        for (let post of this.posts) {
          post.date = new Date(post.date).toDateString();
        }
      },
      err => console.error(err),
      () => console.log('done loading posts')
    );
  }

  createPost() {
    this._blogPostService.create(this.new_post, this.user.token).subscribe(
       data => {
         // refresh the list
         this.getPosts();
         return true;
       },
       error => {
         console.error('Error saving!');
         return throwError(error);
       }
    );
  }


}
