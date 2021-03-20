import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {UserService} from './user.service';

@Injectable()
export class BlogPostService {

  constructor(private http: HttpClient, private _userService: UserService) {
  }

   list() {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
      return this.http.get('/api/posts', httpOptions);
  }

  create(post: any) {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    return this.http.post('/api/posts', JSON.stringify(post), httpOptions);
  }

  delete(id: any) {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    return this.http.delete('/api/posts/' + id, httpOptions);
  }

  edit(id: any, post: any) {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    return this.http.put('/api/posts/' + id, {'body': post}, httpOptions);
  }
}
