import { RouteModule } from './route.module';

describe('RouteModule', () => {
  let routeModule: RouteModule;

  beforeEach(() => {
    routeModule = new RouteModule();
  });

  it('should create an instance', () => {
    expect(routeModule).toBeTruthy();
  });
});
