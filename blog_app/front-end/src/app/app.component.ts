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

  public creating_post: any;

  public deleting_id: any;

  public editing_post:any;

  constructor(private _blogPostService: BlogPostService, public _userService: UserService) { }

  ngOnInit() {
    this.creating_post = {};
    this.editing_post = {};
    this.update()
    this.user = {
      email: '',
      password: ''
    };
  }

  update(){
    this._userService.check();
    this.getPosts();
  }

  login() {
    this._userService.login({'email': this.user.email, 'password': this.user.password}).subscribe(
      ()  => {
          this._userService.is_auth_user = true;
      },
      err => {
        this._userService.errors = err['error'];
      },
      () => {
        this.ngOnInit();
      }
    );
  }

   registration() {
   this._userService.registration({'email': this.user.email, 'username': this.user.username, 'password': this.user.password}).subscribe(
     ()  => {
          this._userService.is_auth_user = true;
      },
      err => {
        this._userService.errors = err['error'];
      },
      () => {
        this.ngOnInit();
      }
    );
  }

  toLogin(){
    this._userService.toLogin();
  }

  toRegistration(){
    this._userService.toRegistration();
  }

  logout() {
    this._userService.logout();
  }

  getPosts() {
    this._blogPostService.list().subscribe(
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
    this._blogPostService.create(this.creating_post).subscribe(
       data => {
         this.creating_post = {}
         this.getPosts();
         return true;
       },
       error => {
         console.error('Error saving!');
         return throwError(error);
       }
    );
  }
  deletePost() {
    this._blogPostService.delete(this.deleting_id).subscribe(
       data => {
         this.deleting_id = ""
         this.getPosts();
         return true;
       },
       error => {
         console.error('Error deleting!');
         return throwError(error);
       }
    );
  }

  editPost() {
    this._blogPostService.edit(this.editing_post.id, this.editing_post.body).subscribe(
       data => {
         this.editing_post = {}
         this.getPosts();
         return true;
       },
       error => {
         console.error('Error deleting!');
         return throwError(error);
       }
    );
  }
}
