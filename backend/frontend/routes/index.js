var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/login', function(req, res, next){
  res.render('login')
});

router.get('/productindividual', function(req, res, next){
  res.render('productindividual')
});

router.get('/products', function(req, res, next){
  res.render('products')
});

router.get('/shoppingBasket', function(req, res, next){
  res.render('shoppingBasket')
});

router.get('/register', function(req, res, next){
  res.render('register')
});

router.get('/checkout', function(req, res, next){
  res.render('checkout')
});

router.get('/confirm', function(req, res, next){
  res.render('confirm')
});

router.get('/orders', function(req, res, next){
  res.render('orders')
});

module.exports = router;