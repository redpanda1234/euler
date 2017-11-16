const theta = .5;

struct (ne, nw, sw, se) {
    ne: (f32, f32),
    nw: (f32, f32),
    sw: (f32, f32),
    se: (f32, f32),
    ctr: (f32, f32),
    slen: f32,

    impl fn contains(self, point: (f32, f32)) {

    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
    }
}
