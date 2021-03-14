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
        'Authorization': 'Bearer ' + this._userService.token// this._userService.token
      })
    };
      return this.http.get('/api/posts', httpOptions);
  }
  // отправка POST запроса для создания нового сообщения в блоге
  create(post: any, token: string) {
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + this._userService.token
      })
    };

    return this.http.post('/api/posts', JSON.stringify(post), httpOptions);
  }

}
