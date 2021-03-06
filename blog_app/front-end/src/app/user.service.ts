import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable()
export class UserService {

  token: any;

  private httpOptions: any;

  public is_auth_user: boolean = false;

  public is_registration: boolean = false;

  public email: string = '';

  public username: string = '';

  public errors: any = [];

  constructor(private http: HttpClient) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})}
  }

  public login(user: { email: any; password: any; }) {
    return this.http.post('/login', JSON.stringify(user), this.httpOptions)
  }

  public registration(user: { email: any; username: any; password: any; }) {
    return this.http.post('/registration', JSON.stringify(user), this.httpOptions);
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
        this.is_auth_user = false
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

}
