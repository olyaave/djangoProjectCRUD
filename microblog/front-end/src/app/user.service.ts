import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable()
export class UserService {

  private httpOptions: any;

  // текущий JWT токен
  public token: string  = '';

  // флаг регистрации
  public is_registration: boolean = false;

  // время окончания жизни токена
  public token_expires: Date = new Date;

  // логин пользователя
  public email: string = '';

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
        if('token' in data)
          this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public registration(user: { email: any; username: any; password: any; }) {
    this.http.post('/registration', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
        if('token' in data)
          this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  // обновление JWT токена
  public refreshToken() {
    this.http.post('/login', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      data => {
        if('token' in data)
          this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public logout() {
    this.token = 'Токен';
    this.token_expires = new Date;
    this.email = '';
  }

  public toLogin(){
    this.is_registration = false;
  }

  public toRegistration(){
    this.is_registration = true;
  }

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

}
