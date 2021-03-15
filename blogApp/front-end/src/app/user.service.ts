import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable()
export class UserService {

  private httpOptions: any;

  // флаг об авторизованности пользователя
  public is_auth_user: boolean = false;

  // флаг регистрации
  public is_registration: boolean = false;

  // логин пользователя
  public email: string = '';

  // логин пользователя
  public username: string = '';

  // сообщения об ошибках авторизации
  public errors: any = [];

  constructor(private http: HttpClient) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
  }

  // используем http.post() для получения токена
  public login(user: { email: any; password: any; }) {
    this.http.post('/login', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
          this.is_auth_user = true
          this.check()
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public registration(user: { email: any; username: any; password: any; }) {
    this.http.post('/registration', JSON.stringify(user), this.httpOptions).subscribe(
      data  => {
          this.is_auth_user = true
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  // обновление JWT токена
  public refreshToken() {
    this.http.post('/login', this.httpOptions).subscribe(
      data => {},
      err => {
        this.errors = err['error'];
      }
    );
  }

    public logout() {
    this.http.delete('/login', this.httpOptions).subscribe(
      data => {
          this.email = '';
          this.username = '';
          this.is_auth_user = false
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

    public check() {
    this.http.get('/api/check', this.httpOptions).subscribe(
      data  => {
        if('username' in data){
          this.username = data['username']
          this.email = data['email']
          this.is_auth_user = true
          }
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public toLogin(){
    this.is_registration = false;
  }

  public toRegistration(){
    this.is_registration = true;
  }


/*
  private updateData(token: string) {
    this.token = token;
    this.errors = [];

    // декодирование токена для получения логина и времени жизни токена

    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    console.log(token_decoded);
    this.email = token_decoded.email;
  }
*/
}
